"""Open-source scene & effect library for Tuya RGB LED strips."""
from .device import Strip
from . import scenes

__all__ = ["Strip", "scenes"]
__version__ = "0.1.0"
