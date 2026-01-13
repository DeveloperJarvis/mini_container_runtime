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
# cgroups MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import os
from mini_container_runtime.logger import setup_logger
from mini_container_runtime.utils import ensure_dir


log = setup_logger("Cgroups")
CGROUP_ROOT = "/sys/fs/cgroup"


# --------------------------------------------------
# cgroup
# --------------------------------------------------
class Cgroup:
    def __init__(self, name: str):
        self.path = os.path.join(CGROUP_ROOT, name)
        ensure_dir(self.path)
    
    def set_memory_limit(self, limit_bytes: int):
        log.info(f"Setting memory limit: {limit_bytes}")
        with open(os.path.join(self.path, "memory.max"), "w") as f:
            f.write(str(limit_bytes))

    def set_cpu_limit(self, quota: int, period: int = 100000):
        log.info(f"Setting CPU limit: quota={quota}")
        with open(os.path.join(self.path, "cpu.max"), "w") as f:
            f.write(f"{quota} {period}")
        
    def add_process(self, pid: int):
        with open(os.path.join(self.path, "cgroup.procs"), "w") as f:
            f.write(str(pid))
