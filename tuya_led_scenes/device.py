"""Thin wrapper over tinytuya for Tuya RGB strips, with scene/music/live helpers.

Credentials are NEVER hard-coded. They come from a config file or environment:
  TUYA_DEVICE_ID, TUYA_LOCAL_KEY, TUYA_ADDRESS   (or a config.ini, see config.example.ini)
"""

from __future__ import annotations

import configparser
import os
import time

import tinytuya

from . import scenes

# Data points for this strip family (product tstgovpmcejfizsy, CORGB3M24).
DP_POWER, DP_MODE, DP_COLOUR, DP_SCENE, DP_MUSIC_MIC = 20, 21, 24, 25, 42


def load_config(path: str | None = None):
    """Return (device_id, address, local_key) from env or an ini file."""
    did = os.environ.get("TUYA_DEVICE_ID")
    key = os.environ.get("TUYA_LOCAL_KEY")
    addr = os.environ.get("TUYA_ADDRESS")
    if did and key and addr:
        return did, addr, key
    cfg = configparser.ConfigParser()
    cfg.read(path or os.environ.get("TUYA_CONFIG", "config.ini"))
    if "device" not in cfg:
        raise SystemExit(
            "No credentials. Set TUYA_DEVICE_ID / TUYA_LOCAL_KEY / TUYA_ADDRESS, "
            "or copy config.example.ini to config.ini and fill it in."
        )
    d = cfg["device"]
    return d["device_id"], d["address"], d["local_key"]


class Strip:
    def __init__(self, device_id=None, address=None, local_key=None, version=3.5):
        if not (device_id and address and local_key):
            device_id, address, local_key = load_config()
        self.dev = tinytuya.Device(device_id, address, local_key)
        self.dev.set_version(version)
        self.dev.set_socketPersistent(True)
        self.dev.set_socketRetryLimit(1)

    def status(self):
        return self.dev.status().get("dps", {})

    def on(self, state=True):
        self.dev.set_value(DP_POWER, state, nowait=False)

    def scene(self, name):
        """Write a named scene into the strip and run it (strip animates itself)."""
        sid, stops = scenes.SCENES[name]
        self.dev.set_value(DP_SCENE, scenes.encode(sid, stops), nowait=False)
        self.dev.set_value(DP_MODE, "scene", nowait=False)

    def music(self, name="music_energetic"):
        """Sound-reactive mode using the strip's built-in mic."""
        self.dev.set_value(DP_MUSIC_MIC, scenes.MUSIC[name], nowait=False)
        self.dev.set_value(DP_MODE, "music", nowait=False)

    def colour(self, h, s=1000, v=1000):
        self.dev.set_value(DP_MODE, "colour", nowait=False)
        self.dev.set_value(DP_COLOUR, f"{h:04x}{s:04x}{v:04x}", nowait=False)

    def live_colour(self, h, s=1000, v=1000):
        """Fast update for live effects (no wait); ~14/s over Wi-Fi."""
        self.dev.set_value(DP_COLOUR, f"{h:04x}{s:04x}{v:04x}", nowait=True)

    def rainbow(self, seconds=20, fps=14):
        self.dev.set_value(DP_MODE, "colour", nowait=False)
        steps = int(seconds * fps)
        for i in range(steps):
            self.live_colour(int((i * 360 / fps) % 360))
            time.sleep(1 / fps)

    def close(self):
        self.dev.close()
