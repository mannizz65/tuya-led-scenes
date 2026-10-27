# tuya-led-scenes

An open-source scene & effect library for **Tuya Wi-Fi RGB LED strips**,
controlled **fully locally** (no cloud). Built by reverse-engineering a
Conecto CORGB3M24 (Tuya product `tstgovpmcejfizsy`), it should work with other
single-zone Tuya RGB strips that use the same data points.

It gives a budget Tuya strip the kind of scenes you get on expensive strips:
sunrise, sunset, rainbow, fire, ocean, aurora, party, police, candle and more,
plus sound-reactive **music** modes using the strip's built-in microphone.

## Why this exists

I bought this strip thinking it would sync with my TV. It never really did — the
app's "music" mode was underwhelming and there was no proper ambient or scene
support. It sat in a drawer and I was about to throw it away.

Instead, I took it apart (over the network, not with a screwdriver), figured out
how it actually talks, and gave it the scenes and effects I wanted in the first
place. A near-useless strip turned into a genuinely fun light. If you have the
same strip gathering dust, this is for you.

> **Single-zone strips only.** This controls the whole strip as one colour at a
> time. Per-pixel / "RGBIC" chase effects need an addressable strip and a
> controller like [WLED](https://kno.wled.ge/). See `PROTOCOL.md`.

## Install

```sh
pip install tinytuya
git clone https://github.com/<you>/tuya-led-scenes
cd tuya-led-scenes
cp config.example.ini config.ini     # then fill in your device id, key and IP
```

Get your device id and **local key** with `python -m tinytuya wizard`
(Tuya IoT developer account), and the IP from your router.

## Use

```sh
python -m tuya_led_scenes list                # all scenes and music presets
python -m tuya_led_scenes scene sunset        # play a scene (the strip runs it itself)
python -m tuya_led_scenes music music_disco   # sound-reactive, built-in mic
python -m tuya_led_scenes colour 240 1000 800 # solid colour (hue sat val)
python -m tuya_led_scenes rainbow 30          # live rainbow driven from the computer
python -m tuya_led_scenes off
```

Or from Python:

```python
from tuya_led_scenes import Strip
s = Strip()            # reads config.ini or TUYA_* env vars
s.scene("aurora")
s.music("music_soft")
s.close()
```

## Scenes

sunrise · sunset · rainbow · ocean · forest · fire · candle · aurora · party ·
romantic · christmas · police · chill · spring · disco · nightlight · reading · daylight

## Music presets

music_energetic · music_soft · music_spectrum · music_warm · music_disco

## How it works

A scene is written into the strip's own memory (data point 25), so the strip
plays the animation itself without the computer. Live effects stream colours to
data point 24 (~14 updates/second over Wi-Fi). The full protocol is in
[`PROTOCOL.md`](PROTOCOL.md).

## Disclaimer

This project is **not affiliated with, endorsed by, or connected to Tuya or
Conecto**. It is an independent, interoperability tool for controlling LED
strips **you own**, using **your own** device key, entirely on your local
network. Reverse-engineering for interoperability is generally permitted (e.g.
the EU Software Directive), but you are responsible for your own use.

Use at your own risk. Talking to the device locally or changing its settings
**may void the manufacturer's warranty**. The authors are not liable for any
damage. All product names and trademarks belong to their respective owners.

## License

MIT — see [LICENSE](LICENSE). Not affiliated with Tuya or Conecto.
