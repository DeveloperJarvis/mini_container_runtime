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
# test_namespaces MODULE
# --------------------------------------------------

# --------------------------------------------------
# imports
# --------------------------------------------------
import pytest
from mini_container_runtime import namespaces
import subprocess
from unittest.mock import patch


def test_namespace_flags_are_ints():
    assert isinstance(namespaces.CLONE_NEWNS, int)
    assert isinstance(namespaces.CLONE_NEWPID, int)
    assert isinstance(namespaces.CLONE_NEWUTS, int)


def test_invalid_hostname_rejected():
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            1, ["hostname", "bad_hostname"]
        )
        with pytest.raises(subprocess.CalledProcessError):
            namespaces.set_hostname("bad_hostname")

def test_valid_hostname_passes(monkeypatch):
    called = {}

    def fake_run(cmd, check):
        called["hostname"] = cmd[1]
        return

    with patch("subprocess.run", fake_run):
        namespaces.set_hostname("valid-host")

    assert called["hostname"] == "valid-host"
