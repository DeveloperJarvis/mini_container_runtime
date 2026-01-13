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
# test_runtime MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import pytest
from mini_container_runtime.runtime import MiniRuntime
from mini_container_runtime.container import Container


def test_runtime_requires_root(monkeypatch):
    monkeypatch.setattr("os.geteuid", lambda: 1000)
    with pytest.raises(PermissionError):
        MiniRuntime()


def test_run_container_creates_container(monkeypatch):
    monkeypatch.setattr("os.geteuid", lambda: 0)

    created = {}

    def fake_run(self):
        created["container"] = self
    
    monkeypatch.setattr(Container, "run", fake_run)

    runtime = MiniRuntime()
    runtime.run_container(
        command=["/bin/echo", "hello"],
        rootfs="/tmp/rootfs",
        hostname='test-container',
    )

    c = created["container"]
    assert c.command == ["/bin/echo", "hello"]
    assert c.rootfs == "/tmp/rootfs"
    assert c.hostname == "test-container"
