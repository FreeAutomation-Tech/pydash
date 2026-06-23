# PyDash

[![Test](https://github.com/FreeAutomation-Tech/pydash/actions/workflows/test.yml/badge.svg)](https://github.com/FreeAutomation-Tech/pydash/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/badge/PyPI-pydash-blue)](https://pypi.org/project/pydash/)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Beautiful terminal system dashboard** — CPU, RAM, disk, network, and top processes, all rendered in real-time with `rich`.

```
┌──────────────────────────────────────────────────────────────────┐
│  PyDash — Terminal System Dashboard  v1.0.0                     │
├──────────────┬───────────────────────────────────────────────────┤
│  System      │  Disk                                             │
│  Uptime: 3d  │  Mount    Usage                   Used    Free   │
│  Load: 0.5   │  /        ███████░░░  72%        45.2GB  18.1GB  │
│  Users: 2    │  /home    ██░░░░░░░░  18%        12.1GB  55.0GB  │
│  Procs: 327  │                                                   │
├──────────────┼───────────────────────────────────────────────────┤
│  CPU         │  Network                                          │
│  ████████░░  │  IP (eth0): 192.168.1.42                         │
│  Per Core    │  Sent:     1.2 GB                                 │
│  ██ ██ ██ ██ │  Received: 3.5 GB                                 │
├──────────────┼───────────────────────────────────────────────────┤
│  Memory      │  Top Processes                                    │
│  RAM ████░░  │  PID   Name          CPU%   MEM%                 │
│  Used: 8/16GB│  1234  python        45.2   12.3                 │
│  Swap ░░░░░░ │  5678  chrome        12.1    8.9                 │
└──────────────┴───────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
pip install pydash
```

```bash
# Full live dashboard
pydash

# Specific panels
pydash cpu
pydash mem
pydash disk
pydash net
pydash ps
pydash sys

# Custom refresh interval (default: 2s)
pydash -i 5
```

---

## Features

- **Live-updating dashboard** — auto-refresh every 2 seconds
- **6 panels**: System info, CPU (per-core), Memory, Disk, Network, Top Processes
- **Color-coded** — each panel has a distinct color theme
- **Zero config** — just install and run
- **Subcommands** — view individual panels without the full dashboard
- **Lightweight** — uses `psutil` + `rich`, no heavy dependencies

---

## Usage

### Full Dashboard

```bash
pydash
```

Hit `Ctrl+C` to exit.

### Individual Panels

```bash
pydash cpu       # CPU usage with per-core breakdown
pydash mem       # RAM and swap usage
pydash disk      # Disk usage per mount point
pydash net       # Network I/O and IP addresses
pydash ps        # Top 10 processes by CPU
pydash sys       # System uptime, load, users
```

---

## What Each Panel Shows

| Panel | Contents |
|-------|----------|
| **System** | Uptime, load average (1/5/15 min), logged-in users, total processes |
| **CPU** | Total usage %, per-core usage bars, physical/logical cores, frequency |
| **Memory** | RAM usage bar, total/used/available, swap usage |
| **Disk** | Per-mountpoint usage bars, used/free space |
| **Network** | IP addresses by interface, total sent/received bytes and packets |
| **Processes** | Top 10 processes by CPU usage: PID, name, CPU%, MEM% |

---

## Why PyDash?

- **htop alternative** — less complex, prettier, Python-native
- **Quick system check** — one command, all the info
- **Remote servers** — works over SSH (no GUI needed)
- **CI/automation** — `pydash sys` for load/uptime in scripts
- **Screenshots** — looks great in blog posts and demos

---

## Development

```bash
git clone https://github.com/FreeAutomation-Tech/pydash.git
cd pydash
pip install -r requirements.txt
python -m pytest tests/ -v
```

---

## License

MIT
