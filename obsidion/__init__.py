import asyncio as _asyncio
import sys as _sys

MIN_PYTHON_VERSION = (3, 8, 1)

__all__ = [
    "MIN_PYTHON_VERSION",
    "__version__",
    "_update_event_loop_policy",
]

__version__ = "0.3.0.dev1"

# check wether the bot can run
if _sys.version_info < MIN_PYTHON_VERSION:
    print(
        f"Python {'.'.join(map(str, MIN_PYTHON_VERSION))} is required to run Obsidion, but you have "
        f"{_sys.version}! Please update Python."
    )
    _sys.exit(1)


def _update_event_loop_policy():
    if _sys.implementation.name == "cpython":
        # Let's not force this dependency, uvloop is much faster on cpython
        try:
            import uvloop as _uvloop
        except ImportError:
            pass
        else:
            _asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())
