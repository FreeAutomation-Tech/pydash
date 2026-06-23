import time
from rich.live import Live
from rich.layout import Layout
from rich import print as rprint

from .panels import (
    get_cpu_panel,
    get_memory_panel,
    get_disk_panel,
    get_network_panel,
    get_process_panel,
    get_system_panel,
)


def _make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="top", size=3),
        Layout(name="main"),
        Layout(name="footer", size=1),
    )
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    layout["left"].split_column(
        Layout(name="system"),
        Layout(name="cpu"),
        Layout(name="memory"),
    )
    layout["right"].split_column(
        Layout(name="disk"),
        Layout(name="network"),
        Layout(name="processes"),
    )
    return layout


HEADER = """
[bold cyan]╔══════════════════════════════════════════════════════════════╗[/bold cyan]
[bold cyan]║[/bold cyan]  [bold yellow]PyDash[/bold yellow] — Terminal System Dashboard  v1.0.0          [bold cyan]║[/bold cyan]
[bold cyan]╚══════════════════════════════════════════════════════════════╝[/bold cyan]"""

FOOTER = "[dim]Press Ctrl+C to exit • Auto-refresh every 2s[/dim]"


def run_dashboard(interval: int = 2):
    layout = _make_layout()

    with Live(auto_refresh=False, screen=True) as live:
        try:
            while True:
                layout["top"].update(HEADER)
                layout["footer"].update(FOOTER)
                layout["system"].update(get_system_panel())
                layout["cpu"].update(get_cpu_panel())
                layout["memory"].update(get_memory_panel())
                layout["disk"].update(get_disk_panel())
                layout["network"].update(get_network_panel())
                layout["processes"].update(get_process_panel())

                live.update(layout, refresh=True)
                time.sleep(interval)
        except KeyboardInterrupt:
            pass
