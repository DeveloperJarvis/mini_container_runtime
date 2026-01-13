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
# namespaces MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import os
import subprocess
from mini_container_runtime.logger import setup_logger


log = setup_logger("Namespaces")


# Linux namespace flags
CLONE_NEWNS     = 0x00020000
CLONE_NEWPID    = 0x20000000
CLONE_NEWUTS    = 0x04000000
CLONE_NEWNET    = 0x40000000
CLONE_NEWPIC    = 0x08000000


def unshare(namespaces):
    """
    Unshare namespaces using the `unshare` syscall wrapper.
    """
    flags = 0
    for ns in namespaces:
        flags |= ns
    
    log.info(f"Unsharing namespaces: {namespaces}")
    os.unshare(flags)


def set_hostname(hostname: str):
    log.info(f"Setting hostname: {hostname}")
    subprocess.run(["hostname", hostname], check=True)
