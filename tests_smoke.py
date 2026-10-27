"""Offline smoke test: encodings are well-formed (no device needed)."""
from tuya_led_scenes import scenes

def test_all_scenes_encode():
    for name, (sid, stops) in scenes.SCENES.items():
        hx = scenes.encode(sid, stops)
        assert len(hx) % 2 == 0 and int(hx, 16) >= 0, name
        assert len(hx) >= 2 + 26, name  # id + at least one 13-byte stop

def test_music_presets():
    for name, hx in scenes.MUSIC.items():
        assert hx.startswith("010101") and len(hx) % 2 == 0, name

if __name__ == "__main__":
    test_all_scenes_encode(); test_music_presets(); print("smoke tests passed")
