import argparse
from unittest.mock import patch

from src.cli import main


class TestCLI:
    def test_default_command(self):
        with patch("sys.argv", ["pydash"]):
            with patch("src.cli.run_dashboard") as mock:
                main()
                mock.assert_called_once()

    def test_cpu_command(self):
        with patch("sys.argv", ["pydash", "cpu"]):
            with patch("src.cli._show_panel") as mock:
                main()
                mock.assert_called_once()

    def test_mem_command(self):
        with patch("sys.argv", ["pydash", "mem"]):
            with patch("src.cli._show_panel") as mock:
                main()
                mock.assert_called_once()

    def test_disk_command(self):
        with patch("sys.argv", ["pydash", "disk"]):
            with patch("src.cli._show_panel") as mock:
                main()
                mock.assert_called_once()

    def test_net_command(self):
        with patch("sys.argv", ["pydash", "net"]):
            with patch("src.cli._show_panel") as mock:
                main()
                mock.assert_called_once()

    def test_ps_command(self):
        with patch("sys.argv", ["pydash", "ps"]):
            with patch("src.cli._show_panel") as mock:
                main()
                mock.assert_called_once()

    def test_sys_command(self):
        with patch("sys.argv", ["pydash", "sys"]):
            with patch("src.cli._show_panel") as mock:
                main()
                mock.assert_called_once()

    def test_custom_interval(self):
        with patch("sys.argv", ["pydash", "-i", "5"]):
            with patch("src.cli.run_dashboard") as mock:
                main()
                mock.assert_called_once_with(5)
