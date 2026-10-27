"""Scene library for Tuya RGB LED strips (work_mode 'scene', DP 25 'scene_data').

Each scene is a list of colour stops; encode() turns them into the device's
hex format, reverse-engineered from the Conecto CORGB3M24 (product tstgovpmcejfizsy):

  scene_data = scene_id(1B) + stops
  stop       = switch_dur(1B) grad_dur(1B) mode(1B) h(2B) s(2B) v(2B) white_bright(2B) temp(2B)
  mode: 0 static, 1 jump, 2 gradient      durations: 0..255, lower = faster
  colour stop -> set h/s/v (s,v are 0..1000), white stop -> h=s=v=0, set bright/temp
"""

STATIC, JUMP, GRADIENT = 0, 1, 2


def _stop(h=0, s=0, v=0, bright=0, temp=0, mode=GRADIENT, sw=0x46, gr=0x46):
    return f"{sw:02x}{gr:02x}{mode:02x}{h:04x}{s:04x}{v:04x}{bright:04x}{temp:04x}"


def colour(h, s=1000, v=1000, mode=GRADIENT, speed=0x46):
    return _stop(h=h, s=s, v=v, mode=mode, sw=speed, gr=speed)


def white(bright=1000, temp=500, mode=STATIC, speed=0x0e):
    return _stop(bright=bright, temp=temp, mode=mode, sw=speed, gr=speed)


def encode(scene_id, stops):
    return f"{scene_id:02x}" + "".join(stops)


# hue shorthands
RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, PINK, MAGENTA = 0, 25, 50, 120, 180, 240, 275, 320, 300

# Common scenes, like the presets on expensive strips. speed: lower = faster.
SCENES = {
    "sunrise":   (0x11, [colour(265, 1000, 120), colour(ORANGE, 1000, 600), colour(30, 700, 1000), white(1000, 600)]),
    "sunset":    (0x12, [colour(ORANGE, 1000, 1000), colour(PINK, 900, 900), colour(275, 900, 700), colour(BLUE, 1000, 500)]),
    "rainbow":   (0x13, [colour(h, 1000, 1000, speed=0x30) for h in (0, 50, 120, 180, 240, 300)]),
    "ocean":     (0x14, [colour(200, 1000, 900), colour(BLUE, 1000, 1000), colour(CYAN, 900, 800), colour(220, 1000, 700)]),
    "forest":    (0x15, [colour(100, 1000, 900), colour(GREEN, 1000, 1000), colour(140, 900, 700), colour(80, 800, 800)]),
    "fire":      (0x16, [colour(RED, 1000, 1000, JUMP, 0x14), colour(12, 1000, 900, JUMP, 0x14),
                          colour(ORANGE, 1000, 1000, JUMP, 0x14), colour(8, 1000, 700, JUMP, 0x14)]),
    "candle":    (0x17, [colour(28, 900, 900, JUMP, 0x28), colour(33, 850, 1000, JUMP, 0x28), colour(25, 950, 700, JUMP, 0x28)]),
    "aurora":    (0x18, [colour(GREEN, 1000, 900, speed=0x50), colour(CYAN, 1000, 800), colour(PURPLE, 900, 900), colour(160, 1000, 700)]),
    "party":     (0x19, [colour(h, 1000, 1000, JUMP, 0x0a) for h in (0, 60, 120, 180, 240, 300)]),
    "romantic":  (0x1a, [colour(PINK, 900, 900, speed=0x5a), colour(RED, 1000, 800), colour(MAGENTA, 900, 900), colour(330, 1000, 700)]),
    "christmas": (0x1b, [colour(RED, 1000, 1000, JUMP, 0x3c), colour(GREEN, 1000, 1000, JUMP, 0x3c)]),
    "police":    (0x1c, [colour(RED, 1000, 1000, JUMP, 0x06), colour(BLUE, 1000, 1000, JUMP, 0x06)]),
    "chill":     (0x1d, [colour(190, 600, 700, speed=0x64), colour(275, 500, 700), colour(320, 500, 700), colour(150, 500, 700)]),
    "spring":    (0x1e, [colour(PINK, 700, 1000), colour(YELLOW, 800, 1000), colour(GREEN, 700, 900), colour(300, 600, 900)]),
    "disco":     (0x1f, [colour(h, 1000, 1000, JUMP, 0x08) for h in (300, 180, 60, 240, 120, 0)]),
    "nightlight":(0x20, [white(150, 550, STATIC)]),
    "reading":   (0x21, [white(1000, 500, STATIC)]),
    "daylight":  (0x22, [white(1000, 1000, STATIC)]),
}


# Music / sound-reactive presets (work_mode 'music', DP 42 mic data).
# mic_data = 010101 00 sens(1B) bright(1B) + up to 3 colours as hue(2B)+sat(2B)
def mic_data(colours, sensitivity=50, bright=100):
    """Built-in-mic sound-reactive data: header, sensitivity, brightness, then
    up to 3 colour stops as hue(2B) + saturation(2B, 0..1000)."""
    out = f"01010100{sensitivity:02x}{bright:02x}"
    for h, s in colours:
        out += f"{h:04x}{s:04x}"
    return out


MUSIC = {
    "music_energetic": mic_data([(0, 1000), (120, 1000), (240, 1000)], sensitivity=0x50, bright=0x64),
    "music_soft":      mic_data([(30, 600), (320, 600), (275, 600)], sensitivity=0x28, bright=0x50),
    "music_spectrum":  mic_data([(0, 1000), (60, 1000), (180, 1000)], sensitivity=0x46, bright=0x64),
    "music_warm":      mic_data([(20, 700), (0, 800), (40, 700)], sensitivity=0x3c, bright=0x5a),
    "music_disco":     mic_data([(300, 1000), (180, 1000), (55, 1000)], sensitivity=0x64, bright=0x64),
}
