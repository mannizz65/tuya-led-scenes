# Protocol notes (reverse-engineered)

Tuya RGB strip, product `tstgovpmcejfizsy` (Conecto CORGB3M24). Local protocol
3.5 via [tinytuya](https://github.com/jasonacox/tinytuya). All values below were
derived by reading the device's own state and the factory scene presets.

## Data points (DPs)

| DP | Name | Type | Meaning |
|----|------|------|---------|
| 20 | power | bool | on/off |
| 21 | work_mode | enum | `white` / `colour` / `scene` / `music` |
| 24 | colour | hex | `HHHHSSSSVVVV` — hue 0–360, sat 0–1000, value 0–1000 |
| 25 | scene_data | hex | the current scene definition (see below) |
| 26 | countdown | int | seconds |
| 27 | music_data | hex | music mode colour data (app/stream driven) |
| 28 | control_data | hex | **write-only live channel**, same colour fields, no flash wear |
| 42 | mic music data | hex | built-in-mic sound reaction (see below) |

Only one local TCP connection (port 6668) is allowed at a time.

## scene_data (DP 25)

```
scene_id (1 byte) + one or more colour stops
stop = switch_dur(1) grad_dur(1) mode(1) hue(2) sat(2) val(2) white_bright(2) color_temp(2)
```

* `mode`: `00` static, `01` jump, `02` gradient (smooth fade)
* `switch_dur` / `grad_dur`: 0–255, lower = faster
* colour stop: set hue/sat/val, leave bright/temp `0000`
* white stop: hue/sat/val `0000`, set bright (0–1000) and color_temp (0–1000)

Example (factory "Soft"): `04 464602007803e803e800000000 464602007803e8000a00000000`

## Mic music data (DP 42)

```
01 01 01 00 sensitivity(1) brightness(1) + up to 3 colours as hue(2) sat(2)
```

Byte 2 is the mic on/off switch (`01`/`00`). Higher sensitivity = reacts to
quieter sound.

## Live colour

Set `work_mode` to `colour`, then stream `HHHHSSSSVVVV` to DP 24. ~14
updates/second over Wi-Fi is smooth. DP 28 (`control_data`) is the intended
no-wear channel for this.
