# BOM — Princeton Reverb (AA1164) Filter Cap Board

Rev F electrical design. Quantities are **per board**.

> **Scope:** only the parts that live *on this board* — the four filter caps,
> the bleeder, and the ground star link. The dropping resistors (1 k / 4.7 k /
> 10 k) between nodes stay on the amp's eyelet board and are **not** part of this
> BOM; they appear in the SPICE model (`sim/`) only to reproduce the node
> voltages.

## Filter capacitors

All electrolytics: aluminium, radial, **≥ 500 V**, **105 °C**, 7.5 mm pitch.
Anchor family: **Nichicon UCY** (voltage code `2H` = 500 V, `M` = ±20 %).
Confirm the exact case-size suffix at the distributor — it varies with µF.

| Ref | Node | Value | Rating | Suggested P/N | Qty |
|-----|------|------:|--------|---------------|:---:|
| C1 | A — B+1 reservoir / 6V6 plates | 47 µF | 500 V 105 °C | Nichicon UCY2H470MHD (16 × 40 mm) | 1 |
| C2 | B — B+2 screens | 22 µF | 500 V 105 °C | Nichicon UCY2H220M&lt;suffix&gt; | 1 |
| C3 | C — B+3 PI / reverb driver | 22 µF | 500 V 105 °C | Nichicon UCY2H220M&lt;suffix&gt; | 1 |
| C4 | D — B+4 preamp / reverb recovery | 33 µF | 500 V 105 °C | Nichicon UCY2H330M&lt;suffix&gt; | 1 |

- C1 bumped to 47 µF to firm the low end (stays under the GZ34's ~60 µF
  input-cap limit).
- C4 footprint laid out to accept **up to 47 µF** so node D stays retunable.
- 22 µF on C2/C3 is the stock value — more capacitance there buys nothing
  audible (confirmed by `sim/`: C/D ripple is already single-digit mV).

## Bleeder

| Ref | Value | Rating | Notes | Qty |
|-----|------:|--------|-------|:---:|
| R1, R2 | 100 kΩ | 2 W, ≥ 350 V | In series = 200 kΩ across node A → GND-PWR | 2 |

Metal-oxide / flameproof, axial. ~0.9 W total across node A, split (~0.45 W
each). Drains node A at power-off; downstream nodes drain through the amp's
dropping resistors while the board is connected. **Still meter every section to
zero before servicing.**

## Grounding / hardware

These are **board features**, not purchased parts (except the standoffs) —
listed so nothing is missed at layout.

| Ref | Item | Notes | Qty |
|-----|------|-------|:---:|
| P1–P4 | B+ wire-entry pads (PTH) | ~1.6 mm finished hole / ~3.3 mm pad, in a row on the fiber-board-facing edge; existing B+ wires poke up and solder in. | 4 |
| GND-PWR, GND-PRE | Ground wire-entry pads (PTH) + chassis lug | Separate dirty (A·B) and clean (C·D) returns; meet at the star. | 2 |
| JP1 | Star link (net-tie) | Joins GND-PWR ↔ GND-PRE at one point. Fit a wire/0 Ω link for single-point tie; omit to run dual returns to the amp's own buses. | 0–1 |
| — | Mounting standoffs + screws | Both mount holes isolated from copper (or make exactly one the ground tie) to avoid a ground loop. | 2 ea |

## Bare board

| Item | Spec |
|------|------|
| PCB | FR-4, 2-layer, 1.6 mm, 1 oz Cu, ~55–60 × 48 mm. Within JLCPCB & OSH Park 2-layer rules. |

---

*Part numbers are suggestions, not the only valid choice — any radial
electrolytic at ≥ 500 V / 105 °C in the right µF and a 7.5 mm pitch / ≤ 16 mm
diameter case will fit. Verify the case suffix and physical size against the
footprint before ordering.*
