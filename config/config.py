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
# config MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import os


# --------------------------------------------------
# config
# --------------------------------------------------
class Config:
    """
    Central configuration for Mini Container Runtime
    """

    # Runtime defaults
    DEFAULT_CGROUP_CPU_LIMIT = os.getenv("MCR_CPU_LIST", "100%")
    DEFAULT_CGROUP_MEMORY_LIST = os.getenv("MCR_MEMORY_LIMIT", "512M")
    DEFAULT_CONTAINER_ROOT = os.getenv("MCR_ROOT_FS", "/var/lib/mcr")
    DEFAULT_NETWORK_NAMESPACE = os.getenv("MCR_NET_NS", "host")

    # Logging
    LOG_LEVEL = os.getenv("MCR_LOG_LEVEL", "INFO")
    PROJECT_DIR = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..",
        ))
    LOG_FILE = os.path.join(PROJECT_DIR, "logs",
                            "mini_container.log")
    
    # Heartbeat / monitoring
    HEARTBEAT_INTERVAL = int(os.getenv(
        "MCR_HEARTBEAT_INTERVAL", "5"
    ))

    # Container execution
    DEFAULT_TIMEOUT_SECONDS = int(os.getenv(
        "MCR_DEFAULT_TIMEOUT", "60"
    ))
