"""Main tests."""
from obsidion import __version__


def test_version() -> None:
    """Mock version."""
    assert __version__ == "1.0.0"
