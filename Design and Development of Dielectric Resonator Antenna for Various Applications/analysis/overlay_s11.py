"""Overlay a simulated (HFSS CSV) and a measured (VNA Touchstone/CSV) S11 curve.

Example:
    python -m analysis.overlay_s11 \
        --sim  results/data/zirconia_cdra_s11_hfss.csv \
        --meas results/measurements/zirconia_cdra.s1p \
        --out  results/figures/comparison/zirconia_sim_vs_meas.png
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .s11_tools import load_hfss_csv, load_touchstone_s1p, summarize_s11


def _load(path: str):
    return load_touchstone_s1p(path) if path.lower().endswith(".s1p") else load_hfss_csv(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sim", required=True, help="HFSS CSV export (Freq [GHz], dB(S(1,1)))")
    ap.add_argument("--meas", required=True, help="VNA .s1p or CSV with the same two columns")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fmin", type=float, default=5.3)
    ap.add_argument("--fmax", type=float, default=6.0)
    args = ap.parse_args()

    fig, ax = plt.subplots(figsize=(7, 4.2))
    for label, path, color in (("Simulated (HFSS)", args.sim, "#3d405b"), ("Measured (VNA)", args.meas, "#e07a5f")):
        f, s = _load(path)
        r = summarize_s11(f, s)
        bw = f"{r.bandwidth_mhz:.0f} MHz" if r.bandwidth_mhz else "n/a"
        ax.plot(f, s, color=color, lw=2,
                label=f"{label}: {r.s11_min_db:.1f} dB @ {r.f_res_ghz:.3f} GHz, -10 dB BW {bw}")
    ax.axhline(-10, color="grey", ls=":", lw=1)
    ax.set_xlim(args.fmin, args.fmax)
    ax.set_xlabel("Frequency (GHz)")
    ax.set_ylabel("|S11| (dB)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.out, dpi=200)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
