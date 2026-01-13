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
# test_cgroups MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import os
from mini_container_runtime.cgroups import Cgroup


def test_cgroup_path_created(tmp_path, monkeypatch):
    fake_root = tmp_path / "cgroup"
    monkeypatch.setattr(
        "mini_container_runtime.cgroups.CGROUP_ROOT",
        str(fake_root)
    )

    cg = Cgroup("testgroup")
    assert os.path.isdir(cg.path)


def test_cgroup_add_process(tmp_path, monkeypatch):
    fake_root = tmp_path / "cgroup"
    monkeypatch.setattr(
        "mini_container_runtime.cgroups.CGROUP_ROOT",
        str(fake_root)
    )

    cg = Cgroup("testgroup")
    procs = os.path.join(cg.path, "cgroup.procs")

    cg.add_process(1234)
    
    with open(procs) as f:
        assert f.read().strip() == "1234"
