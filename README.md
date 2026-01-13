# Mini Container Runtime

**Mini Container Runtime** is a lightweight Python library that allows you to start isolated “containers” on Linux using namespaces, process isolation, and resource management. This project demonstrates fundamental containerization concepts, including PID, UTS, NET, and MNT namespaces, along with basic cgroup-based resource control.

---

## 🏃🏻‍♂️How to Run (Linux only)

```bash
# create environment
python3 -m venv .env
# enable environment
source .env/bin/active

# run setup
python3 -m pip install -e .

# creating /tmp/rootfs
sudo mkdir -p /tmp/rootfs/{bin,lib,lib64}
sudo cp /bin/sh /tmp/rootfs/bin/

# lld
ldd /bin/sh
# # Output
# linux-vdso.so.1 (0x00007ffd399ad000)
# libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007c05cfe00000)
# /lib64/ld-linux-x86-64.so.2 (0x00007c05d01f4000)

# copy and move more
sudo cp /lib/x86_64-linux-gnu/libc.so.6 /tmp/rootfs/lib/
sudo cp /lib64/ld-linux-x86-64.so.2 /tmp/rootfs/lib64/

# run examples
sudo $(which python3) examples/run_simple_container.py
```

**Note:** Only for linux

---

## 🧪 How to run tests

```bash
source .envlin/bin/activate
pytest -v
```

---

## Features

- Isolated **process namespace** for container processes
- Isolated **hostname (UTS)** and **network stack (NET)**
- Isolated **filesystem (MNT)** with support for `chroot` / `pivot_root`
- Optional **IPC and USER namespace isolation**
- Resource constraints via **cgroups** (CPU, memory, PIDs)
- Lightweight, Python-based, no external dependencies
- Simple API for starting, stopping, and monitoring containers

---

## Prerequisites

- Linux system with kernel ≥ 3.8 (supports namespaces & cgroups v2)
- Python 3.10+
- Root privileges (for full namespace and chroot operations)

> Note: Some namespaces (like USER) may allow unprivileged usage depending on kernel configuration.

---

## Installation

```bash
git clone https://github.com/DeveloperJarvis/mini-container-runtime.git
cd mini-container-runtime
pip install .
```

---

## Usage

### Start a Container

```python
from mini_container_runtime import ContainerRuntime

runtime = ContainerRuntime()
container = runtime.run(
    image="/path/to/rootfs",   # Path to container root filesystem
    command=["/bin/sh"],       # Command to execute
    cpu_limit=50,              # Optional CPU limit (%)
    memory_limit=256*1024*1024 # Optional Memory limit (bytes)
)
```

### Stop a Container

```python
runtime.stop(container.id)
```

### Check Status

```python
status = runtime.status(container.id)
print(f"Container {container.id} is {status}")
```

---

## Design Overview

- **CLI / Runtime Manager**
  Handles user commands, container metadata, and lifecycle management.

- **Container Engine**
  Responsible for:

  - Forking processes
  - Creating Linux namespaces (`PID`, `UTS`, `NET`, `MNT`, `IPC`, `USER`)
  - Applying cgroup-based resource limits
  - Setting up filesystem isolation (`chroot`/`pivot_root`)
  - Launching the user-specified process

- **Container Process**
  The isolated child process that runs the requested command inside its own namespace and resource boundaries.

---

## Supported Namespaces

| Namespace | Purpose                              |
| --------- | ------------------------------------ |
| PID       | Isolates process IDs                 |
| UTS       | Isolates hostname                    |
| NET       | Isolates network stack               |
| MNT       | Isolates filesystem mounts           |
| IPC       | Isolates inter-process communication |
| USER      | Allows mapping of user/group IDs     |

---

## Limitations

- Currently supports only Linux systems.
- Minimal networking support (no bridge networking by default).
- Requires root for full isolation in some namespaces.
- No container image management yet; root filesystem must be prepared manually.

---

## License

This project is licensed under the **GNU General Public License v3.0**.
See [LICENSE](https://www.gnu.org/licenses/) for more details.

---

## Author

**Developer Jarvis** (Pen Name)
GitHub: [https://github.com/DeveloperJarvis](https://github.com/DeveloperJarvis)
