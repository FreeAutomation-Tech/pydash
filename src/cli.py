import argparse
import sys

from .panels import (
    get_cpu_panel,
    get_memory_panel,
    get_disk_panel,
    get_network_panel,
    get_process_panel,
    get_system_panel,
)
from .dashboard import run_dashboard


def _show_panel(getter, title: str):
    from rich.console import Console
    console = Console()
    header = f"[bold cyan]PyDash[/bold cyan] — {title}"
    console.print(header)
    console.print("=" * 50)
    console.print(getter())


def main():
    parser = argparse.ArgumentParser(
        description="PyDash — Beautiful terminal system dashboard",
        usage="pydash [command] [options]",
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="dash",
        choices=["dash", "cpu", "mem", "memory", "disk", "net", "network", "ps", "processes", "sys", "system"],
        help="Dashboard or specific panel (default: dash)",
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=2,
        help="Refresh interval in seconds (default: 2)",
    )

    args = parser.parse_args()

    cmd = args.command

    if cmd == "dash":
        run_dashboard(args.interval)
    elif cmd == "cpu":
        _show_panel(get_cpu_panel, "CPU Usage")
    elif cmd in ("mem", "memory"):
        _show_panel(get_memory_panel, "Memory Usage")
    elif cmd == "disk":
        _show_panel(get_disk_panel, "Disk Usage")
    elif cmd in ("net", "network"):
        _show_panel(get_network_panel, "Network")
    elif cmd in ("ps", "processes"):
        _show_panel(get_process_panel, "Top Processes")
    elif cmd in ("sys", "system"):
        _show_panel(get_system_panel, "System Info")


if __name__ == "__main__":
    main()
