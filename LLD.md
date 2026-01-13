# **Mini Container Runtime - LLD**

**Goal:** Start isolated “containers” using Linux namespaces, cgroups, and basic process isolation from Python.

---

## **1. High-Level Architecture**

```
 ┌──────────────────────────────┐
 │      Container Runtime       │
 │  (Python CLI / Manager)     │
 └─────────────┬────────────────┘
               │
               ▼
 ┌──────────────────────────────┐
 │      Container Engine        │
 │ - Namespaces Setup           │
 │ - Cgroups Setup              │
 │ - Filesystem Mounts          │
 │ - Process Fork & Exec        │
 └─────────────┬────────────────┘
               │
               ▼
 ┌──────────────────────────────┐
 │      Container Process       │
 │ - Isolated PID/UTS/NET/...  │
 │ - Own Filesystem (chroot)   │
 │ - User-specified Command     │
 └──────────────────────────────┘
```

---

## **2. Key Components**

### **A. CLI / Runtime Manager**

- Accepts user commands:

  - `run <image> <command>`
  - `exec <container_id> <command>`

- Manages container metadata (ID, process PID, state)
- Handles logging and status

### **B. Container Engine**

- Responsible for **spawning isolated processes** with OS-level isolation
- **Sub-components:**

  1. **Namespace Manager**

     - Use Linux namespaces for isolation:

       - **PID namespace** → process tree isolated
       - **UTS namespace** → container hostname isolation
       - **NET namespace** → network stack isolation
       - **MNT namespace** → separate filesystem mounts
       - **IPC namespace** → IPC isolation
       - **USER namespace** → user and group mapping

  2. **Cgroups Manager**

     - Limit container resources:

       - CPU shares
       - Memory limit
       - PIDs limit

  3. **Filesystem Manager**

     - Set up container filesystem:

       - Use **chroot** or **pivot_root**
       - Mount `/proc`, `/sys`, `/dev`
       - Optional: overlay filesystem for read-only base images

  4. **Process Launcher**

     - Fork a new process
     - Unshare namespaces
     - Set cgroup limits
     - Change root filesystem
     - Exec the user command

### **C. Container Process**

- The **isolated child process**
- Runs user-specified command
- PID 1 inside PID namespace
- Has its own hostname, mounts, network stack
- Logs exit status to runtime manager

---

## **3. Data Structures**

### **Container Metadata**

- Container ID (UUID)
- Host PID
- Namespaces used
- Cgroup path
- Root filesystem path
- Status (`RUNNING`, `EXITED`)
- Start/Stop timestamp

### **Resource Limits**

- CPU shares
- Memory limit
- PIDs limit

---

## **4. Execution Flow**

**Step 1: Runtime CLI**

- User runs: `minicontainer run alpine /bin/sh`
- CLI parses image, command, options

**Step 2: Container Engine**

- Create **container metadata**
- Fork process
- In child:

  1. `unshare()` namespaces (PID, UTS, MNT, NET, IPC, USER)
  2. Apply cgroup limits
  3. Set hostname
  4. Change root filesystem (`chroot` / `pivot_root`)
  5. Mount `/proc`, `/sys`, `/dev`
  6. Execute target command

**Step 3: Parent Process**

- Tracks child PID
- Updates container state
- Handles stop/kill

**Step 4: Container Process**

- PID 1 in its PID namespace
- Executes command
- Exits → runtime manager collects exit code

---

## **5. Isolation Techniques**

| Feature       | Technique                    |
| ------------- | ---------------------------- |
| Process PID   | `unshare(CLONE_NEWPID)`      |
| Hostname      | `unshare(CLONE_NEWUTS)`      |
| Network       | `unshare(CLONE_NEWNET)`      |
| Filesystem    | `chroot` / `pivot_root`      |
| IPC           | `unshare(CLONE_NEWIPC)`      |
| Users/Groups  | `unshare(CLONE_NEWUSER)`     |
| Resource Ctrl | cgroups v2 (`cpu`, `memory`) |

---

## **6. Optional Enhancements**

- **Image Support**

  - Extract tarball rootfs for container

- **Networking**

  - Use virtual Ethernet pairs + NAT

- **Volumes**

  - Bind host directories into container

- **Logging**

  - Capture stdout/stderr into container logs

- **Lifecycle**

  - Start / Stop / Kill / Restart containers

---

## **7. Python Integration**

- Use `ctypes` or `subprocess` + `unshare` syscall
- `os.fork()` → child sets up namespaces
- `os.execvp()` → run user command
- Optional: `py-cgroups` for resource management

---

### **8. Summary**

- Lightweight container runtime = **process isolation + resource limits**
- Key OS primitives:

  - `fork()`, `exec()`
  - `unshare()` for namespaces
  - `chroot()` / `pivot_root()` for FS isolation
  - cgroups for resource control

- Python orchestrates the runtime, metadata, and lifecycle

# Mini Container Runtime — Extended LLD

## Goals

Extend the runtime to support:

1. **User namespaces (rootless containers)**
2. **Network namespaces + veth**
3. **Seccomp syscall filtering**
4. **OverlayFS root filesystem**
5. **Container lifecycle states**
6. **Docker-style JSON runtime spec**

Design constraints:

- Linux only
- Uses kernel primitives (namespaces, cgroups, seccomp)
- Python as orchestrator (syscalls via `os`, `ctypes`, `subprocess`)
- Separation of _policy_ vs _mechanism_

---

## 1. User Namespaces (Rootless Containers)

### Problem Solved

Allow containers to run **without root**, while processes inside believe they are UID 0.

### Design

#### Namespace

- `CLONE_NEWUSER`

#### UID/GID Mapping

- Map container UID 0 → host unprivileged UID
- Same for GID

#### Required Files

- `/proc/<pid>/uid_map`
- `/proc/<pid>/gid_map`
- `/proc/<pid>/setgroups`

#### Component

**`namespaces.py`**

- `create_user_namespace()`
- `write_uid_map(pid, uid_map)`
- `write_gid_map(pid, gid_map)`

#### Flow

1. Parent forks child
2. Child pauses
3. Parent writes UID/GID mappings
4. Child continues execution as “root”

#### Security Notes

- No access to host root
- Cannot load kernel modules
- Limited device access

---

## 2. Network Namespace + veth

### Problem Solved

Each container gets its **own network stack**.

### Namespace

- `CLONE_NEWNET`

### Architecture

```
Host Network Namespace
 ├── veth-host <─────┐
 │                   │
 └── bridge (optional)
                     │
Container Network Namespace
 └── veth-container
```

### Components

**`namespaces.py`**

- Network namespace creation

**`network.py` (new)**

- veth pair creation
- IP assignment
- Namespace move
- Loopback setup

### Lifecycle

1. Create veth pair
2. Move one end into container netns
3. Assign IP addresses
4. Bring interfaces up
5. Optional bridge/NAT

### Rootless Limitation

- Full networking requires:

  - `slirp4netns` OR
  - root helper

- Design should abstract network driver:

  - `BridgeDriver`
  - `SlirpDriver`

---

## 3. Seccomp Filtering

### Problem Solved

Restrict available syscalls → reduce attack surface.

### Model

- **Allowlist-based seccomp filter**
- Default: `SCMP_ACT_KILL`

### Component

**`seccomp.py` (new)**

Responsibilities:

- Load syscall allowlist
- Generate BPF filter
- Apply via `prctl()` or `seccomp()`

### Policy Examples

- Allow: `read`, `write`, `exit`, `futex`
- Deny: `mount`, `ptrace`, `kexec`

### Spec Integration

Seccomp profile loaded from JSON spec.

---

## 4. OverlayFS Root Filesystem

### Problem Solved

Fast, copy-on-write root filesystem like Docker.

### Filesystem Layout

```
/containers/<id>/
 ├── lower/   (image)
 ├── upper/   (container writes)
 ├── work/
 └── merged/  (mount target)
```

### Component

**`filesystem.py`**

Responsibilities:

- Prepare overlay directories
- Mount overlayfs
- Chroot / pivot_root
- Cleanup on exit

### Mount Type

```
overlay
lowerdir=lower,
upperdir=upper,
workdir=work
```

### Advantages

- Immutable images
- Cheap container startup
- Snapshot-friendly

---

## 5. Container Lifecycle States

### States

```
CREATED
STARTING
RUNNING
PAUSED
STOPPED
EXITED
DEAD
```

### State Transitions

| From     | To       | Trigger             |
| -------- | -------- | ------------------- |
| CREATED  | STARTING | run()               |
| STARTING | RUNNING  | exec success        |
| RUNNING  | PAUSED   | SIGSTOP             |
| PAUSED   | RUNNING  | SIGCONT             |
| RUNNING  | EXITED   | process exit        |
| ANY      | DEAD     | unrecoverable error |

### Component

**`container.py`**

Responsibilities:

- State tracking
- PID management
- Exit code capture
- Signal handling

### Persistence

- Store state as JSON under:

  ```
  /containers/<id>/state.json
  ```

---

## 6. Docker-Style JSON Spec

### Purpose

Decouple **runtime engine** from **container configuration**.

### Spec File (`container.json`)

Key sections:

- `process`
- `rootfs`
- `mounts`
- `linux.namespaces`
- `linux.cgroups`
- `linux.seccomp`
- `network`

### Component

**`spec.py` (new)**

Responsibilities:

- Parse JSON
- Validate schema
- Convert spec → runtime actions

### Runtime Usage

```
spec = load_spec("container.json")
container = Container(spec)
container.start()
```

### Compatibility Goal

- Rough OCI alignment
- Not full OCI compliance (by design)

---

## Component Interaction Diagram

```
runtime.py
 └── container.py
      ├── namespaces.py
      ├── filesystem.py
      ├── cgroups.py
      ├── seccomp.py
      ├── network.py
      └── spec.py
```

---

## Security Model Summary

| Feature         | Protection        |
| --------------- | ----------------- |
| User namespaces | No host root      |
| Seccomp         | Syscall sandbox   |
| Cgroups         | Resource limits   |
| Net namespace   | Network isolation |
| OverlayFS       | FS immutability   |

---

## What This Demonstrates (Interview Value)

✅ Kernel namespace mastery
✅ Rootless container design
✅ Real Docker internals knowledge
✅ Secure-by-default architecture
✅ Clear separation of concerns
✅ Production-grade extensibility

---

## Next Logical Steps (Optional)

If you want, I can next:

- Generate **OCI-compatible JSON schema**
- Add **capabilities dropping**
- Add **image builder**
- Add **checkpoint/restore (CRIU)**
- Add **CLI (`mini-run`, `mini-ps`)**
- Add **architecture diagrams (ASCII / Mermaid)**

Just tell me how deep you want to go 🚀
