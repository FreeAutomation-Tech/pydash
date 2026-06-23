import psutil
from rich.table import Table
from rich.text import Text
from rich.progress_bar import ProgressBar
from rich.panel import Panel
from rich.columns import Columns
from rich import box


def _bar(percent: float, width: int = 20) -> str:
    filled = int(percent / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[green]{bar}[/green]"


def get_cpu_panel() -> Panel:
    cpu_percent = psutil.cpu_percent(interval=0.1)
    per_cpu = psutil.cpu_percent(interval=0, percpu=True)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_column("Metric", style="cyan")
    table.add_column("Value")

    bar = _bar(cpu_percent)
    table.add_row("Total Usage", f"{bar}  {cpu_percent:.1f}%")
    table.add_row("Physical Cores", str(psutil.cpu_count(logical=False)))
    table.add_row("Logical Cores", str(cpu_count))
    if cpu_freq:
        table.add_row("Frequency", f"{cpu_freq.current:.0f} MHz")

    per_cpu_str = " ".join(f"{p:3.0f}%" for p in per_cpu)
    per_cpu_bars = "  ".join(_bar(p, 4) for p in per_cpu)
    table.add_row("Per Core", f"{per_cpu_bars}\n{per_cpu_str}")

    return Panel(table, title="[bold yellow]CPU[/bold yellow]", border_style="yellow")


def get_memory_panel() -> Panel:
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_column("Metric", style="cyan")
    table.add_column("Value")

    mem_bar = _bar(mem.percent)
    table.add_row("RAM", f"{mem_bar}  {mem.percent:.1f}%")
    table.add_row("Total", _format_bytes(mem.total))
    table.add_row("Used", _format_bytes(mem.used))
    table.add_row("Available", _format_bytes(mem.available))
    table.add_row("", "")
    swap_bar = _bar(swap.percent)
    table.add_row("Swap", f"{swap_bar}  {swap.percent:.1f}%")
    table.add_row("Swap Used", _format_bytes(swap.used))
    table.add_row("Swap Total", _format_bytes(swap.total))

    return Panel(table, title="[bold green]Memory[/bold green]", border_style="green")


def get_disk_panel() -> Panel:
    partitions = psutil.disk_partitions()
    disk_usage = []
    for p in partitions:
        try:
            usage = psutil.disk_usage(p.mountpoint)
            disk_usage.append((p.mountpoint, usage))
        except PermissionError:
            continue

    table = Table(show_header=True, box=box.SIMPLE, padding=(0, 1))
    table.add_column("Mount", style="cyan")
    table.add_column("Usage")
    table.add_column("Used", justify="right")
    table.add_column("Free", justify="right")

    for mount, usage in disk_usage:
        bar = _bar(usage.percent, 10)
        table.add_row(
            mount,
            f"{bar}  {usage.percent:.0f}%",
            _format_bytes(usage.used),
            _format_bytes(usage.free),
        )

    total_usage = psutil.disk_usage("/")
    return Panel(
        table,
        title=f"[bold magenta]Disk[/bold magenta] ({_format_bytes(total_usage.total)} total)",
        border_style="magenta",
    )


def get_network_panel() -> Panel:
    net = psutil.net_io_counters()
    addrs = psutil.net_if_addrs()

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_column("Metric", style="cyan")
    table.add_column("Value")

    interfaces = list(addrs.keys())[:4]
    for iface in interfaces:
        ips = [a.address for a in addrs[iface] if a.family == 2]
        if ips:
            table.add_row(f"IP ({iface})", ips[0])

    table.add_row("", "")
    table.add_row("Sent", _format_bytes(net.bytes_sent))
    table.add_row("Received", _format_bytes(net.bytes_recv))
    table.add_row("Packets Sent", f"{net.packets_sent:,}")
    table.add_row("Packets Recv", f"{net.packets_recv:,}")

    return Panel(table, title="[bold blue]Network[/bold blue]", border_style="blue")


def get_process_panel() -> Panel:
    processes = sorted(psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]),
                       key=lambda p: p.info["cpu_percent"] or 0, reverse=True)[:10]

    table = Table(show_header=True, box=box.SIMPLE, padding=(0, 1))
    table.add_column("PID", style="dim", justify="right")
    table.add_column("Name")
    table.add_column("CPU%", justify="right")
    table.add_column("MEM%", justify="right")

    for proc in processes:
        try:
            table.add_row(
                str(proc.info["pid"]),
                proc.info["name"][:20] or "?",
                f"{proc.info['cpu_percent'] or 0:.1f}",
                f"{proc.info['memory_percent'] or 0:.1f}",
            )
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return Panel(table, title="[bold red]Top Processes[/bold red]", border_style="red")


def get_system_panel() -> Panel:
    boot_time = psutil.boot_time()
    from datetime import datetime
    uptime = datetime.now() - datetime.fromtimestamp(boot_time)
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60

    load_avg = psutil.getloadavg()
    users = psutil.users()

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
    table.add_column("Metric", style="cyan")
    table.add_column("Value")
    table.add_row("Uptime", f"{days}d {hours}h {minutes}m")
    table.add_row("Load (1/5/15)", f"{load_avg[0]:.2f} / {load_avg[1]:.2f} / {load_avg[2]:.2f}")
    table.add_row("Users", str(len(users)))
    table.add_row(" processes", str(len(psutil.pids())))

    return Panel(table, title="[bold white]System[/bold white]", border_style="white")


def _format_bytes(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if value < 1024:
            return f"{value:.1f} {unit}"
        value /= 1024
    return f"{value:.1f} PB"
