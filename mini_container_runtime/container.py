# --------------------------------------------------
# -*- Python -*- Compatibility Header
#
# Copyright (C) 2023 Developer Jarvis (Pen Name)
#
# This file is part of the Mini Container Runtime Library. This library is free
# software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Mini Container Runtime - Start isolated "containers" using namespaces (Linux)
#               Skills: OS internals, syscalls, process management
#
# Author: Developer Jarvis (Pen Name)
# Contact: https://github.com/DeveloperJarvis
#
# --------------------------------------------------

# --------------------------------------------------
# container MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import os
import subprocess
from mini_container_runtime.logger import setup_logger
from mini_container_runtime import namespaces
from mini_container_runtime.filesystem import setup_rootfs
from mini_container_runtime.cgroups import Cgroup


log = setup_logger("Container")


# --------------------------------------------------
# container
# --------------------------------------------------
class Container:
    def __init__(
        self,
        command,
        rootfs="/tmp/mini_rootfs",
        hostname="mini_container",
        memory_limit=None,
        cpu_quota=None,
    ):
        self.command = command
        self.rootfs = rootfs
        self.hostname = hostname
        self.memory_limit = memory_limit
        self.cpu_quota = cpu_quota
    
    def run(self):
        log.info("Starting container")

        namespaces.unshare([
            namespaces.CLONE_NEWNS,
            namespaces.CLONE_NEWPID,
            namespaces.CLONE_NEWUTS,
        ])

        pid = os.fork()
        if pid == 0:
            # Child (Container init)
            namespaces.set_hostname(self.hostname)
            setup_rootfs(self.rootfs)

            log.info(f"Executing command: {self.command}")
            os.execvp(self.command[0], self.command)
        else:
            # Parent
            if self.memory_limit or self.cpu_quota:
                cg = Cgroup(f"mini_{pid}")
                if self.memory_limit:
                    cg.set_memory_limit(self.memory_limit)
                if self.cpu_quota:
                    cg.set_cpu_limit(self.cpu_quota)
                cg.add_process(pid)
            
            os.waitpid(pid, 0)
            log.info("Container exited")
