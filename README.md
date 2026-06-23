# can_cap_boards

A repo to contain different PCBs with associated gerber files and SPICE sim docs.

The theme: small interior-mount boards that retire vintage multi-section
twist-lock "can" electrolytics in tube amps, replacing them with discrete,
individually serviceable modern radial caps.

> ⚠️ These boards carry **lethal B+ voltages** (400 V+). Discharge and meter
> every section to zero before handling. See each board's README.

## Boards

| Board | Amp | What it replaces | Status |
|-------|-----|------------------|--------|
| [`princeton_reverb_aa1164`](princeton_reverb_aa1164/) | Fender Princeton Reverb (AA1164) | 4-section can → 47/22/22/33 µF | design + BOM + SPICE + KiCad project (DRC-clean starter) + gerbers |

Each board folder contains its own `README.md` (design notes), `BOM.md`, an
illustrated `design_reference.html` (schematic + mechanical drawings), a `sim/`
directory with the SPICE supply model, and a `kicad/` directory with the KiCad
sources and `kicad/fab/` fabrication outputs (gerbers, drill, BOM, position).

## License

Apache-2.0 (see [`LICENSE`](LICENSE)).
