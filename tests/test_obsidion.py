"""Main tests."""

from obsidion import __version__


def test_version() -> None:
    """Mock version."""
    assert __version__ == "0.3.1"
