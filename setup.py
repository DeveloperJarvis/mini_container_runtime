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
# setup MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
from setuptools import setup, find_packages


setup(
    name="mini_container_runtime",
    version="0.1.0",
    description="A minimal container runtime using Linux namespaces and cgroups",
    author="Developer Jarvis",
    author_email="developerjarvis@github.com",
    url="https://github.com/DeveloperJarvis/mini_container_runtime",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        # Add dependencies if needed
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
        ],
    },
    entry_points={
        "console_scripts": [
            "mcr_run=mini_container_runtime.runtime:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
)
