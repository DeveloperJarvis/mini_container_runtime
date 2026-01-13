## Project structure

---

mini-container-runtime/
├── README.md
├── LICENSE
├── setup.py # Installation script
├── pyproject.toml # Optional, modern packaging
├── requirements.txt # Optional dependencies
├── config/
│ ├── **init**.py
│ └── settings.py # Configuration like default limits, paths
├── mini_container_runtime/
│ ├── **init**.py
│ ├── runtime.py # Core container runtime manager
│ ├── container.py # Container process abstraction
│ ├── namespaces.py # Functions for creating and managing Linux namespaces
│ ├── cgroups.py # Resource limitation helpers
│ ├── filesystem.py # chroot/pivot_root and mount helpers
│ ├── logger.py # Logging utilities
│ └── utils.py # Misc helpers (e.g., ID generation, validation)
├── examples/
│ ├── run_simple_container.py # Minimal example to start a container
│ └── resource_limits.py # Example showing cgroup CPU/memory limits
├── tests/
│ ├── **init**.py
│ ├── test_runtime.py
│ ├── test_namespaces.py
│ ├── test_cgroups.py
│ └── test_filesystem.py
└── docs/
├── architecture.md # LLD / diagrams of runtime
└── design_notes.md # Notes on namespaces, cgroups, limitations

```

### Structure Explanation

* **`mini_container_runtime/`**: Core library code. Each major aspect of the container runtime has its own module:

  * `runtime.py` → manages container lifecycle
  * `container.py` → abstraction of a single container process
  * `namespaces.py` → PID/UTS/NET/MNT/IPC/USER namespace setup
  * `cgroups.py` → apply resource limits
  * `filesystem.py` → isolation of filesystem
  * `logger.py` → structured logging
  * `utils.py` → helpers for IDs, validation, etc.

* **`config/`**: Centralized settings for defaults, e.g., heartbeat interval, default memory/cpu limits.

* **`examples/`**: Practical usage examples for testing and demos.

* **`tests/`**: Unit tests for each component.

* **`docs/`**: Design documentation, architecture diagrams, and LLD notes.

* **Root files**: Standard packaging, README, LICENSE, and optional requirements.

```
