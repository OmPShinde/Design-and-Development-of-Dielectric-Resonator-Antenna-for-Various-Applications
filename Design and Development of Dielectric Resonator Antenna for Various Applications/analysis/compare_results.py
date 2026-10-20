"""Build comparison tables and charts from results/data/results_summary.json.

Usage:  python -m analysis.compare_results
Writes: results/figures/comparison/*.png  and  results/data/comparison_table.md
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data" / "results_summary.json"
OUT_FIG = ROOT / "results" / "figures" / "comparison"
OUT_TABLE = ROOT / "results" / "data" / "comparison_table.md"

KEYS = ["circular_patch", "alumina_cdra", "zirconia_cdra"]
COLORS = ["#8d99ae", "#e07a5f", "#3d405b"]


def load() -> dict:
    with open(DATA) as fh:
        return json.load(fh)


def markdown_table(sim: dict) -> str:
    rows = [
        ("Resonant frequency (GHz)", "f_res_ghz", "{:.3f}"),
        ("Minimum S11 (dB)", "s11_min_db", "{:.2f}"),
        ("VSWR at resonance", "vswr", "{:.3g}"),
        ("-10 dB bandwidth (MHz)", "bandwidth_mhz", "{:g}"),
        ("-10 dB bandwidth (%)", "bandwidth_percent", "{:.2f}"),
        ("Realized gain at fr (dBi)", "realized_gain_at_fr_dbi", "{:.1f}"),
        ("Peak realized gain (dBi)", "peak_realized_gain_dbi", "{:.2f}"),
        ("Radiation efficiency at fr (%)", "efficiency_at_fr_percent", "{:.1f}"),
        ("Peak directivity, 3D (dBi)", "peak_directivity_dbi", "{:.1f}"),
        ("Main beam", "main_beam", "{}"),
        ("Radiator volume (mm^3)", "radiator_volume_mm3", "{:,}"),
    ]
    head = "| Parameter | " + " | ".join(sim[k]["label"] for k in KEYS) + " |"
    sep = "|---|" + "---|" * len(KEYS)
    lines = [head, sep]
    for name, key, fmt in rows:
        cells = []
        for k in KEYS:
            v = sim[k].get(key)
            cells.append("-" if v is None else fmt.format(v))
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def bar_figure(sim: dict) -> Path:
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    panels = [
        ("Minimum S11 (dB)", "s11_min_db", False),
        ("Radiation efficiency at fr (%)", "efficiency_at_fr_percent", False),
        ("Realized gain at fr (dBi)", "realized_gain_at_fr_dbi", False),
        ("-10 dB bandwidth (MHz)", "bandwidth_mhz", False),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.8))
    labels = ["Patch", "Alumina", "Zirconia"]
    for ax, (title, key, _) in zip(axes, panels):
        vals = [sim[k][key] for k in KEYS]
        bars = ax.bar(labels, vals, color=COLORS)
        ax.set_title(title, fontsize=10)
        ax.bar_label(bars, fmt="%.4g", fontsize=9, padding=2)
        ax.margins(y=0.18)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Simulated performance at 5.8 GHz (HFSS)", fontsize=12)
    fig.tight_layout()
    path = OUT_FIG / "performance_comparison.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def volume_figure(sim: dict) -> Path:
    OUT_FIG.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(4.5, 3.8))
    labels = ["Alumina", "Zirconia"]
    vals = [sim["alumina_cdra"]["radiator_volume_mm3"], sim["zirconia_cdra"]["radiator_volume_mm3"]]
    bars = ax.bar(labels, vals, color=COLORS[1:])
    ax.set_yscale("log")
    ax.bar_label(bars, fmt="%d", padding=2)
    ax.set_ylabel("Resonator volume (mm$^3$, log scale)")
    ax.set_title("Resonator volume on the same 60x60 mm board", fontsize=10)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    path = OUT_FIG / "volume_comparison.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def main() -> None:
    data = load()
    sim = data["simulated"]
    OUT_TABLE.write_text(markdown_table(sim))
    print(f"wrote {OUT_TABLE.relative_to(ROOT)}")
    print(f"wrote {bar_figure(sim).relative_to(ROOT)}")
    print(f"wrote {volume_figure(sim).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
