from src.panels import _format_bytes, _bar


class TestFormatBytes:
    def test_bytes(self):
        assert _format_bytes(0) == "0.0 B"
        assert _format_bytes(500) == "500.0 B"

    def test_kilobytes(self):
        result = _format_bytes(2048)
        assert "KB" in result

    def test_megabytes(self):
        result = _format_bytes(1048576)
        assert "MB" in result or "GB" in result

    def test_gigabytes(self):
        result = _format_bytes(1073741824)
        assert "GB" in result

    def test_terabytes(self):
        result = _format_bytes(1099511627776)
        assert "TB" in result


class TestBar:
    def test_bar_zero(self):
        result = _bar(0)
        assert "░" in result
        assert "█" not in result or result.count("█") == 0

    def test_bar_full(self):
        result = _bar(100)
        assert "█" in result

    def test_bar_half(self):
        result = _bar(50, 10)
        assert "█" in result
        assert "░" in result

    def test_bar_custom_width(self):
        result = _bar(50, 5)
        assert len(result.replace("[green]", "").replace("[/green]", "")) == 5


class TestPanelsImport:
    def test_cpu_panel_importable(self):
        from src.panels import get_cpu_panel
        assert callable(get_cpu_panel)

    def test_memory_panel_importable(self):
        from src.panels import get_memory_panel
        assert callable(get_memory_panel)

    def test_disk_panel_importable(self):
        from src.panels import get_disk_panel
        assert callable(get_disk_panel)

    def test_network_panel_importable(self):
        from src.panels import get_network_panel
        assert callable(get_network_panel)

    def test_process_panel_importable(self):
        from src.panels import get_process_panel
        assert callable(get_process_panel)

    def test_system_panel_importable(self):
        from src.panels import get_system_panel
        assert callable(get_system_panel)
