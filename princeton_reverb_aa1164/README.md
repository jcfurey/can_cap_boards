# Princeton Reverb (AA1164) — Filter Cap Board

Interior-mount filter board that retires the original 4-section twist-lock "can"
electrolytic in the blackface Fender Princeton Reverb (AA1164) and close clones,
replacing it with discrete, individually serviceable, modern radial electrolytics.

Mounts inside the chassis among the existing circuitry, with the wire-entry holes
on the edge facing the fiber/eyelet board so the existing B+ wiring lands straight
across. The empty can knockout is covered separately (blanking plate / plug).

> ⚠️ **High voltage.** B+ on the reservoir node sits near **420 VDC** in operation,
> and downstream nodes float up toward it during warm-up. Treat the whole board as
> lethal. Discharge and meter every section to zero before handling.

## Design goals

- Electrical drop-in for the stock can, but with individually replaceable caps
- Modern, high-quality radial electrolytics, **≥ 500 V**
- **Split** power / preamp-reverb grounds for low hum, star-tied
- Existing B+ wiring lands on the fiber-board-facing edge

## Filter values

| Node | Function | Value | Rating |
|------|----------|------:|--------|
| A (B+1) | Reservoir — 6V6 plates | 47 µF | 500 V, 105 °C |
| B (B+2) | Screens | 22 µF | 500 V, 105 °C |
| C (B+3) | PI / reverb driver | 22 µF | 500 V, 105 °C |
| D (B+4) | Preamp / reverb recovery | 33 µF | 500 V, 105 °C |

Anchor part: **Nichicon UCY2H470MHD** (47 µF / 500 V / 105 °C, 7.5 mm pitch,
16 × 40 mm). The 22 µF and 33 µF come from the same UCY family — confirm the exact
case suffix/size at the distributor.

Notes:
- Node A reservoir bumped to **47 µF** to firm up the low end (stays under the
  GZ34's ~60 µF input-cap limit).
- Node D laid out to accept up to **47 µF** so it stays retunable with an iron.
- Screens (B) and PI/reverb-driver (C) kept at stock 22 µF — extra capacitance
  there buys nothing audible.

## Grounding — split, star-tied

- **GND-PWR** — dirty returns: caps **A + B** and the bleeder
- **GND-PRE** — clean returns: caps **C + D**
- The two pours meet **only** at a single **star link (JP1)**, which is the single
  chassis tie.
  - Fit JP1 → one ground wire, single-point tie.
  - Omit JP1 → run GND-PWR and GND-PRE to their own amp ground buses for a true
    dual return.
- The rectifier center-tap belongs on the **power** side at the star, never on the
  preamp pour.
- Exactly **one** chassis connection either way — no loops.

If the reverb driver (node C) ever injects buzz, moving just that negative from
GND-PRE to GND-PWR turns this into a 3-way split — it's only a pour assignment.

## Layers & routing (2-layer)

- **Fiber-board face:** B+ traces + wire-entry pads. Traces **~2.5 mm** wide
  (robustness / HV margin, not current); teardrop the pad junctions.
- **Far face:** the two ground pours (GND-PWR / GND-PRE), each pulled back
  **≥ 2.5 mm** from B+.
- Same-layer clearance **≥ 2.5 mm** (3 mm where room allows). Opposite-layer
  isolation through 1.6 mm FR-4 is ample at ~420 V; optionally clear the pour in
  the shadow directly under B+ traces.

### KiCad tips

- GND-PWR and GND-PRE are **separate nets** joined by a **net-tie footprint** at
  JP1 — otherwise DRC flags them as a short.
- Put the four B+ nets in their own **net class** (clearance 2.5 mm, track ~2.5 mm)
  so DRC enforces creepage automatically.

## Mechanical

- Rectangular, ~**55–60 × 48 mm**, FR-4 2-layer, 1.6 mm, **1 oz** copper.
- Caps stand off the far face into open interior — verify ~40 mm depth clearance
  for the 47 µF (or lay caps down if it's tight).
- Mount on standoffs; **both mount holes isolated** from copper (or make exactly
  one the ground tie) to avoid a ground loop.

## Bleeder

2 × 100 kΩ 2 W in series (= 200 kΩ) across node A, returning to GND-PWR. Drains
node A at power-off; downstream nodes drain through the amp's dropping resistors
while the board is connected. **Always meter every section to zero before
servicing.**

## Fabrication

- Within both **JLCPCB** and **OSH Park** 2-layer design rules.
- 1 oz copper is standard at both (meets the ≥ ½ oz target); 2 oz buys little here.
- OSH Park prices by area — keep it ~50 mm. JLCPCB is a flat tier up to
  100 × 100 mm, so size is effectively free there.

## Simulation

_TODO_ — SPICE model of the AA1164 power supply (GZ34 + dropping network) to
verify ripple at each node and sag behavior with the 47/22/22/33 µF set.

## Status

- [x] Electrical design (rev F)
- [ ] KiCad schematic
- [ ] KiCad layout
- [ ] Fabrication outputs (gerbers)
- [ ] SPICE supply sim
- [ ] Built & tested

## License

Apache-2.0 (see repository `LICENSE`).
