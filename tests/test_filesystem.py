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
# test_filesystem MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import pytest
from mini_container_runtime.filesystem import setup_rootfs


def test_setup_rootfs_creates_directory(tmp_path, monkeypatch):
    rootfs = tmp_path / "rootfs"

    monkeypatch.setattr("subprocess.run", lambda *a, **k: None)
    monkeypatch.setattr("os.chroot", lambda _: None)
    monkeypatch.setattr("os.chdir", lambda _: None)

    setup_rootfs(str(rootfs))
    assert rootfs.exists()

