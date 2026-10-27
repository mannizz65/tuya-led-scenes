"""CLI: python -m tuya_led_scenes <command>

  list                       show all scenes and music presets
  scene <name>               play a scene (strip runs it itself)
  music [<preset>]           sound-reactive mode (default: music_energetic)
  colour <hue> [sat] [val]   solid colour (hue 0-360, sat/val 0-1000)
  rainbow [seconds]          live rainbow driven from this computer
  on | off                   power
  status                     print the strip's data points
"""
import sys

from .device import Strip
from . import scenes


def main(argv=None):
    a = (argv or sys.argv[1:])
    if not a or a[0] in ("-h", "--help", "help"):
        print(__doc__)
        return
    cmd = a[0]
    if cmd == "list":
        print("Scenes:", ", ".join(scenes.SCENES))
        print("Music :", ", ".join(scenes.MUSIC))
        return
    s = Strip()
    try:
        if cmd == "scene":
            s.scene(a[1])
        elif cmd == "music":
            s.music(a[1] if len(a) > 1 else "music_energetic")
        elif cmd == "colour":
            s.colour(int(a[1]), int(a[2]) if len(a) > 2 else 1000, int(a[3]) if len(a) > 3 else 1000)
        elif cmd == "rainbow":
            s.rainbow(int(a[1]) if len(a) > 1 else 20)
        elif cmd == "on":
            s.on(True)
        elif cmd == "off":
            s.on(False)
        elif cmd == "status":
            print(s.status())
        else:
            print("unknown command:", cmd); print(__doc__)
    finally:
        s.close()


if __name__ == "__main__":
    main()
