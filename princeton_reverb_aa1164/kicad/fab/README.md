# Fabrication outputs — AA1164 Filter Cap Board

Generated from `../princeton_reverb_aa1164.kicad_pcb` with `kicad-cli` (KiCad 7).
**Regenerated artifacts** — re-export after any board edit.

> ⚠️ This is a *starting* layout — verify mechanical fit and re-run DRC in the
> KiCad GUI before actually ordering. See `../README.md`.

## Contents

| File | What |
|------|------|
| `princeton_reverb_aa1164-gerbers.zip` | All Gerbers + drill, zipped for upload |
| `gerbers/*.gbr` | RS-274X Gerbers (F.Cu, B.Cu, F/B silkscreen, F/B mask, Edge.Cuts) |
| `gerbers/*.drl` | Excellon drill (absolute origin, mm) + `-drl_map.gbr` map |
| `gerbers/*.gbrjob` | Gerber job file |
| `princeton_reverb_aa1164-pos.csv` | Pick-and-place positions (both sides, mm) |
| `princeton_reverb_aa1164-bom.csv` | Grouped BOM (qty / value / footprint / refs) |

All parts are **through-hole**, so the pos/BOM files are mostly for reference,
not automated assembly.

## Suggested fab settings

- 2-layer, **FR-4 1.6 mm**, **1 oz** copper, HASL or ENIG.
- Min track/space on this board is **2.5 mm** — far inside any fab's limits.
- Smallest drill is **1.0 mm** (net-tie / mounting-hole-adjacent); finished
  wire-entry holes are **1.6 mm**.
- Well within both **JLCPCB** and **OSH Park** 2-layer rules (see the board
  `README.md` for the cost trade-off).

## Re-exporting

```sh
cd ..
kicad-cli pcb export gerbers --no-protel-ext \
  --layers "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" -o fab/gerbers/ princeton_reverb_aa1164.kicad_pcb
kicad-cli pcb export drill --format excellon --drill-origin absolute \
  --generate-map --map-format gerberx2 -o fab/gerbers/ princeton_reverb_aa1164.kicad_pcb
kicad-cli pcb export pos --format csv --units mm --side both \
  -o fab/princeton_reverb_aa1164-pos.csv princeton_reverb_aa1164.kicad_pcb
```
