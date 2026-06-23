#!/usr/bin/env python3
"""Generate the Princeton Reverb AA1164 filter-cap-board schematic (KiCad 7).

Connectivity is defined by local labels dropped exactly onto symbol pin
endpoints -- no drawn wires -- which is the most robust way to author a
schematic programmatically. Validated afterwards with `kicad-cli sch erc`
and a netlist export (see check_netlist.py).
"""
import uuid
from kiutils.schematic import Schematic
from kiutils.symbol import Symbol, SymbolLib
from kiutils.items.schitems import (SchematicSymbol, LocalLabel, SymbolProjectInstance,
                                    SymbolProjectPath, HierarchicalSheetInstance)
from kiutils.items.common import Position, Property, Effects, Font

PROJECT = "princeton_reverb_aa1164"
ROOT = str(uuid.uuid4())
SYMDIR = "/usr/share/kicad/symbols"


def uid():
    return str(uuid.uuid4())


# ---- library symbol cache (embedded into the schematic's lib_symbols) --------
_libcache = {}


def load_lib_symbol(lib, name):
    if lib not in _libcache:
        _libcache[lib] = SymbolLib.from_file(f"{SYMDIR}/{lib}.kicad_sym")
    for s in _libcache[lib].symbols:
        if s.entryName == name:
            return s
    raise KeyError(f"{lib}:{name}")


sch = Schematic.create_new()
sch.uuid = ROOT
sch.generator = "generate_sch.py"

# embed each unique library symbol, retargeted to "Lib:Name"
used = [("Device", "C_Polarized"), ("Device", "R"), ("Device", "NetTie_2"),
        ("Connector", "TestPoint"), ("Mechanical", "MountingHole")]
for lib, name in used:
    s = load_lib_symbol(lib, name)
    s.libraryNickname = lib            # -> libId "Lib:Name"
    sch.libSymbols.append(s)

# pin connection points in *library* coords (Y-up), per symbol
PINS = {
    "C_Polarized": {"1": (0.0, 3.81), "2": (0.0, -3.81)},
    "R":          {"1": (0.0, 3.81), "2": (0.0, -3.81)},
    "NetTie_2":   {"1": (-2.54, 0.0), "2": (2.54, 0.0)},
    "TestPoint":  {"1": (0.0, 0.0)},
    "MountingHole": {},
}

nets = {}   # net name -> list of (x,y) endpoints to label


def place(lib, name, ref, value, footprint, x, y, in_bom=True):
    """Place a symbol; return dict of pin-number -> absolute (x,y)."""
    sym = SchematicSymbol(
        libraryNickname=lib, entryName=name,
        position=Position(x, y, 0), unit=1,
        inBom=in_bom, onBoard=True, dnp=False, fieldsAutoplaced=True,
        uuid=uid())
    def prop(k, v, pid, dy, hide=False):
        eff = Effects(font=Font(), hide=hide)
        return Property(key=k, value=v, id=pid, position=Position(x, y + dy, 0), effects=eff)
    sym.properties = [
        prop("Reference", ref, 0, -6.0),
        prop("Value", value, 1, 6.0),
        prop("Footprint", footprint, 2, 0.0, hide=True),
        prop("Datasheet", "~", 3, 0.0, hide=True),
    ]
    sym.pins = {pn: uid() for pn in PINS[name]}
    sym.instances = [SymbolProjectInstance(
        name=PROJECT,
        paths=[SymbolProjectPath(sheetInstancePath="/" + ROOT, reference=ref, unit=1)])]
    sch.schematicSymbols.append(sym)
    abspins = {}
    for pn, (lx, ly) in PINS[name].items():
        abspins[pn] = (round(x + lx, 4), round(y - ly, 4))   # Y-up -> Y-down
    return abspins


def join(net, *pts):
    nets.setdefault(net, []).extend(pts)


# ---- placement ---------------------------------------------------------------
CY = 100.0
CX = {"C1": 50.0, "C2": 80.0, "C3": 110.0, "C4": 140.0}
CAP = "Capacitor_THT:CP_Radial_D16.0mm_P7.50mm"

c1 = place("Device", "C_Polarized", "C1", "47µF", CAP, CX["C1"], CY)
c2 = place("Device", "C_Polarized", "C2", "22µF", CAP, CX["C2"], CY)
c3 = place("Device", "C_Polarized", "C3", "22µF", CAP, CX["C3"], CY)
c4 = place("Device", "C_Polarized", "C4", "33µF", CAP, CX["C4"], CY)

RES = "Resistor_THT:R_Axial_DIN0414_L11.9mm_D4.5mm_P5.08mm_Vertical"
r1 = place("Device", "R", "R1", "100k", RES, 25.0, 96.0)
r2 = place("Device", "R", "R2", "100k", RES, 25.0, 108.0)

WE_B = "wire_entry:WireEntry_BPlus"
WE_G = "wire_entry:WireEntry_GND"
p1 = place("Connector", "TestPoint", "P1", "B+1_A", WE_B, CX["C1"], 85.0)
p2 = place("Connector", "TestPoint", "P2", "B+2_B", WE_B, CX["C2"], 85.0)
p3 = place("Connector", "TestPoint", "P3", "B+3_C", WE_B, CX["C3"], 85.0)
p4 = place("Connector", "TestPoint", "P4", "B+4_D", WE_B, CX["C4"], 85.0)
pgp = place("Connector", "TestPoint", "P5", "GND-PWR", WE_G, 70.0, 120.0)
pgr = place("Connector", "TestPoint", "P6", "GND-PRE", WE_G, 130.0, 120.0)

nt = place("Device", "NetTie_2", "NT1", "STAR", "wire_entry:StarTie_8mm", 100.0, 120.0)

place("Mechanical", "MountingHole", "H1", "MountingHole",
      "MountingHole:MountingHole_3.2mm_M3", 25.0, 130.0, in_bom=False)
place("Mechanical", "MountingHole", "H2", "MountingHole",
      "MountingHole:MountingHole_3.2mm_M3", 160.0, 130.0, in_bom=False)

# ---- nets --------------------------------------------------------------------
join("HV_A", c1["1"], p1["1"], r1["1"])
join("HV_B", c2["1"], p2["1"])
join("HV_C", c3["1"], p3["1"])
join("HV_D", c4["1"], p4["1"])
join("BLEED_MID", r1["2"], r2["1"])
join("GND-PWR", c1["2"], c2["2"], r2["2"], nt["1"], pgp["1"])
join("GND-PRE", c3["2"], c4["2"], nt["2"], pgr["1"])

for net, pts in nets.items():
    for (x, y) in pts:
        sch.labels.append(LocalLabel(
            text=net, position=Position(x, y, 0),
            effects=Effects(font=Font()), uuid=uid()))

sch.sheetInstances = [HierarchicalSheetInstance(instancePath="/", page="1")]

out = f"{PROJECT}.kicad_sch"
sch.to_file(out)
print("wrote", out, "with", len(sch.schematicSymbols), "symbols,",
      len(sch.labels), "labels,", len(nets), "nets")
