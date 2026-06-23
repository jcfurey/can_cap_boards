#!/usr/bin/env python3
"""Build the Princeton Reverb AA1164 filter-cap board PCB (KiCad 7, pcbnew).

Layer plan (matches the design docs):
  F.Cu  - B+ traces (fiber-board-facing side), fat & short, 2.5 mm wide
  B.Cu  - split ground pours: GND-PWR (left, caps A/B + bleeder) and
          GND-PRE (right, caps C/D), joined only at the NT1 net-tie.

Board-wide clearance is 2.5 mm: every net here is either a high-voltage node
or a ground return and we want >=2.5 mm creepage between them everywhere, so a
single default rule enforces the spec. Each B+ wire-entry pad is placed next to
its own cap so the high-voltage traces stay short and never pass another net's
through-hole pad. Runs DRC at the end.

NOTE: this is a *starting* layout - electrically complete and DRC-clean, but
placement/mechanical fit (and regrouping the wire-entry pads into a single edge
row per the mechanical drawing) should be refined in the KiCad GUI.
"""
import pcbnew
from pcbnew import VECTOR2I, FromMM

FP = "/usr/share/kicad/footprints"
PROJ = "wire_entry.pretty"
OUT = "princeton_reverb_aa1164.kicad_pcb"

CAP = ("Capacitor_THT", "CP_Radial_D16.0mm_P7.50mm")
RES = ("Resistor_THT", "R_Axial_DIN0414_L11.9mm_D4.5mm_P5.08mm_Vertical")
WE_B = (PROJ, "WireEntry_BPlus")
WE_G = (PROJ, "WireEntry_GND")
NT = (PROJ, "StarTie_8mm")
MH = ("MountingHole", "MountingHole_3.2mm_M3")

W, H = 60.0, 54.0          # board outline, mm
SPLIT = 33.0               # ground-pour split (x)
GAP = 1.25                 # half of the 2.5 mm zone-to-zone gap at the split
TRACK = 2.5

board = pcbnew.CreateEmptyBoard()
board.SetCopperLayerCount(2)

# ---- nets --------------------------------------------------------------------
NETNAMES = ["HV_A", "HV_B", "HV_C", "HV_D", "BLEED_MID", "GND-PWR", "GND-PRE"]
for n in NETNAMES:
    board.Add(pcbnew.NETINFO_ITEM(board, n))
def net(n):
    return board.FindNet(n)

# ---- board-wide design rules: 2.5 mm clearance + 2.5 mm default track --------
ds = board.GetDesignSettings()
nc = board.GetAllNetClasses()["Default"]
nc.SetClearance(FromMM(2.5)); nc.SetTrackWidth(FromMM(TRACK))
ds.m_CopperEdgeClearance = FromMM(0.3)

footprints = {}
def place(lib, ref, val, x, y, ang=0):
    libpath = lib[0] if lib[0].endswith(".pretty") else f"{FP}/{lib[0]}.pretty"
    fp = pcbnew.FootprintLoad(libpath, lib[1])
    assert fp, f"load failed {lib}"
    libnick = lib[0][:-len(".pretty")] if lib[0].endswith(".pretty") else lib[0]
    fp.SetFPID(pcbnew.LIB_ID(libnick, lib[1]))
    fp.SetReference(ref); fp.SetValue(val)
    fp.SetPosition(VECTOR2I(FromMM(x), FromMM(y)))
    if ang:
        fp.SetOrientationDegrees(ang)
    board.Add(fp)
    footprints[ref] = fp
    return fp

def setnet(ref, padnum, netname):
    footprints[ref].FindPadByNumber(str(padnum)).SetNet(net(netname))

def padpos(ref, padnum):
    return footprints[ref].FindPadByNumber(str(padnum)).GetPosition()

# ---- caps (pad1 = +, footprint origin; pad2 = - is +7.5 mm in x) -------------
# left column = power (A top, B bottom); right column = preamp (C top, D bottom)
place(CAP, "C1", "47uF", 16.25, 16)   # + at 16.25, - at 23.75
place(CAP, "C2", "22uF", 16.25, 40)
place(CAP, "C3", "22uF", 42.25, 16)
place(CAP, "C4", "33uF", 42.25, 40)
for ref, hv in (("C1", "HV_A"), ("C2", "HV_B"), ("C3", "HV_C"), ("C4", "HV_D")):
    setnet(ref, 1, hv)
setnet("C1", 2, "GND-PWR"); setnet("C2", 2, "GND-PWR")
setnet("C3", 2, "GND-PRE"); setnet("C4", 2, "GND-PRE")

# ---- bleeder (vertical 2W resistors), far-left edge, power side ---------------
# ang=270 stacks the chain monotonically down x=6:
#   R1.1 HV_A (13) -> R1.2 MID (18.08) -> R2.1 MID (21) -> R2.2 GND-PWR (26.08)
# so the short BLEED_MID link between the inner pads crosses no other-net pad.
place(RES, "R1", "100k", 6, 11, ang=270)
place(RES, "R2", "100k", 6, 23, ang=270)   # 12 mm apart: clears the ~9 mm courtyard
setnet("R1", 1, "HV_A"); setnet("R1", 2, "BLEED_MID")
setnet("R2", 1, "BLEED_MID"); setnet("R2", 2, "GND-PWR")

# ---- wire-entry pads, each next to its own cap (short B+ traces) --------------
place(WE_B, "P1", "B+1_A", 16.25, 7);  setnet("P1", 1, "HV_A")   # above C1
place(WE_B, "P2", "B+2_B", 16.25, 49); setnet("P2", 1, "HV_B")   # below C2
place(WE_B, "P3", "B+3_C", 42.25, 7);  setnet("P3", 1, "HV_C")   # above C3
place(WE_B, "P4", "B+4_D", 42.25, 49); setnet("P4", 1, "HV_D")   # below C4
place(WE_G, "P5", "GND-PWR", 9, 49);   setnet("P5", 1, "GND-PWR")
place(WE_G, "P6", "GND-PRE", 55, 49);  setnet("P6", 1, "GND-PRE")

# ---- net-tie star (8mm wide: each pad sits well inside its pour) + holes ------
place(NT, "NT1", "STAR", SPLIT - 4, 27)           # pad1 at 29 (PWR), pad2 at 37 (PRE)
setnet("NT1", 1, "GND-PWR"); setnet("NT1", 2, "GND-PRE")
place(MH, "H1", "", 57.5, 9)
place(MH, "H2", "", 57.5, 45)

# ---- board outline (Edge.Cuts) -----------------------------------------------
def edge(x1, y1, x2, y2):
    s = pcbnew.PCB_SHAPE(board); s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(VECTOR2I(FromMM(x1), FromMM(y1))); s.SetEnd(VECTOR2I(FromMM(x2), FromMM(y2)))
    s.SetLayer(pcbnew.Edge_Cuts); s.SetWidth(FromMM(0.15)); board.Add(s)
edge(0, 0, W, 0); edge(W, 0, W, H); edge(W, H, 0, H); edge(0, H, 0, 0)

# ---- routing: short B+ traces on F.Cu -----------------------------------------
def track(netname, a, b, layer=pcbnew.F_Cu, w=TRACK):
    t = pcbnew.PCB_TRACK(board); t.SetStart(a); t.SetEnd(b)
    t.SetWidth(FromMM(w)); t.SetLayer(layer); t.SetNet(net(netname)); board.Add(t)

track("HV_A", padpos("P1", 1), padpos("C1", 1))
track("HV_A", padpos("R1", 1), padpos("P1", 1))   # feed bleeder from the north (via P1), clear of BLEED_MID
track("HV_B", padpos("P2", 1), padpos("C2", 1))
track("HV_C", padpos("P3", 1), padpos("C3", 1))
track("HV_D", padpos("P4", 1), padpos("C4", 1))
track("BLEED_MID", padpos("R1", 2), padpos("R2", 1))

# net-tie pads -> their pours via dedicated B.Cu tracks (pours are pulled back
# from the tie so neither pour fills over the bridge copper)
track("GND-PWR", padpos("NT1", 1), VECTOR2I(FromMM(24), FromMM(27)), layer=pcbnew.B_Cu)
track("GND-PRE", padpos("NT1", 2), VECTOR2I(FromMM(42), FromMM(27)), layer=pcbnew.B_Cu)

# ---- split ground pours on B.Cu (pulled back from the central net-tie) --------
ZL = 26.5   # GND-PWR right edge
ZR = 39.5   # GND-PRE left edge
def zone(netname, pts):
    z = pcbnew.ZONE(board); z.SetLayer(pcbnew.B_Cu); z.SetNet(net(netname))
    z.SetMinThickness(FromMM(0.25))  # clearance comes from the Default netclass (2.5 mm)
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    poly = z.Outline(); poly.NewOutline()
    for (x, y) in pts:
        poly.Append(VECTOR2I(FromMM(x), FromMM(y)))
    board.Add(z); return z

zone("GND-PWR", [(0.5, 0.5), (ZL, 0.5), (ZL, H - 0.5), (0.5, H - 0.5)])
zone("GND-PRE", [(ZR, 0.5), (W - 0.5, 0.5), (W - 0.5, H - 0.5), (ZR, H - 0.5)])

board.Save(OUT)
print("saved (unfilled)", OUT)

# zone fill is reliable only after a save/reload (CreateEmptyBoard leaves the
# filler's internal state uninitialised, which segfaults otherwise)
board = pcbnew.LoadBoard(OUT)
board.BuildConnectivity()
pcbnew.ZONE_FILLER(board).Fill(board.Zones())
board.Save(OUT)
print("filled + saved", OUT)

# ---- DRC ---------------------------------------------------------------------
rpt = "drc.rpt"
pcbnew.WriteDRCReport(board, rpt, pcbnew.EDA_UNITS_MILLIMETRES, True)
import re
txt = open(rpt).read()
viol = re.findall(r'\[(\w+)\]: (.+)', txt)
print("---- DRC summary ----")
print("violations:", len(viol))
for k in sorted(set(v[0] for v in viol)):
    print(f"  {k}: {sum(1 for v in viol if v[0]==k)}")
m = re.search(r'Found (\d+) unconnected', txt)
print("unconnected pads:", m.group(1) if m else "?")
print("\n(full report in drc.rpt)")
