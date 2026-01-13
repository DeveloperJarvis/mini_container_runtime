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
# filesystem MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import os
import subprocess
from mini_container_runtime.logger import setup_logger
from mini_container_runtime.utils import ensure_dir


log = setup_logger("Filesystem")


def setup_rootfs(rootfs: str):
    """
    Prepare minimal filesystem isolation using chroot + mount namespace.
    """
    ensure_dir(rootfs)

    log.info(f"Mounting rootfs: {rootfs}")
    subprocess.run(["mount", "--bind", rootfs, rootfs], check=True)

    os.chdir(rootfs)
    os.chroot(".")
    os.chdir("/")

    log.info("Root filesystem isolated")
