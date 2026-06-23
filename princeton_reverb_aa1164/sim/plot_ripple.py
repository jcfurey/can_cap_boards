#!/usr/bin/env python3
"""Run the AA1164 PSU ngspice deck and plot the steady-state ripple.

Produces aa1164_psu_ripple.png: each B+ node (A..D) over the last few line
cycles, annotated with DC level and pk-pk ripple. The raw ngspice dump
(aa1164_psu_nodes.dat, ~30 MB) is regenerated on each run and removed
afterwards -- it is intentionally not committed (see .gitignore).

Usage:  python3 plot_ripple.py
Requires: ngspice on PATH, numpy, matplotlib.
"""
import os
import subprocess
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.join(HERE, "aa1164_psu.cir")
DATA = os.path.join(HERE, "aa1164_psu_nodes.dat")
PNG = os.path.join(HERE, "aa1164_psu_ripple.png")

WINDOW_S = 0.05  # plot the last 50 ms (6 line cycles @ 120 Hz)
NODES = [("A", "B+1 reservoir / 6V6 plates", "47 uF"),
         ("B", "B+2 screens", "22 uF"),
         ("C", "B+3 PI / reverb driver", "22 uF"),
         ("D", "B+4 preamp / reverb recovery", "33 uF")]


def run_ngspice():
    print("Running ngspice ...")
    subprocess.run(["ngspice", "-b", DECK], check=True, cwd=HERE)
    if not os.path.exists(DATA):
        sys.exit("ngspice did not produce %s" % DATA)


def load():
    # wrdata + wr_singlescale layout: t, V(A), V(B), V(C), V(D)
    raw = np.loadtxt(DATA, skiprows=1)  # first line is the vecnames header
    t = raw[:, 0]
    return t, {name: raw[:, i + 1] for i, (name, _, _) in enumerate(NODES)}


def main():
    run_ngspice()
    t, v = load()
    mask = t >= (t[-1] - WINDOW_S)
    tw = (t[mask] - t[mask][0]) * 1e3  # ms from window start

    fig, axes = plt.subplots(4, 1, figsize=(8, 9), sharex=True)
    for ax, (name, desc, cap) in zip(axes, NODES):
        y = v[name][mask]
        dc = y.mean()
        pp = y.max() - y.min()
        ax.plot(tw, y, lw=1.1)
        ax.axhline(dc, color="0.6", ls="--", lw=0.8)
        unit = "mV" if pp < 1.0 else "V"
        pp_disp = pp * 1e3 if pp < 1.0 else pp
        ax.set_title("Node %s  (%s, %s)   DC=%.1f V   ripple=%.2f %s pk-pk"
                     % (name, desc, cap, dc, pp_disp, unit), fontsize=9)
        ax.set_ylabel("V")
        ax.grid(True, alpha=0.3)
    axes[-1].set_xlabel("time (ms, steady state)")
    fig.suptitle("Princeton Reverb AA1164 PSU - steady-state ripple "
                 "(47/22/22/33 uF board)", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    fig.savefig(PNG, dpi=110)
    print("Wrote %s" % PNG)

    os.remove(DATA)
    print("Removed raw dump %s" % os.path.basename(DATA))


if __name__ == "__main__":
    main()
