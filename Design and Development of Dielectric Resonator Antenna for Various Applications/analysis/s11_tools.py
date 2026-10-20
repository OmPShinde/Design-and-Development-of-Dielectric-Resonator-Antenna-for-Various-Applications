"""Reflection-coefficient utilities and HFSS-export post-processing.

HFSS CSV exports (Results > Export Data) have a header like
``Freq [GHz],dB(S(1,1)) [] - Setup1 : Sweep`` and can be fed straight into
:func:`load_hfss_csv`.
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path


def s11_db_to_vswr(s11_db: float) -> float:
    """Linear VSWR from |S11| in dB (S11 < 0)."""
    gamma = 10.0 ** (s11_db / 20.0)
    if gamma >= 1.0:
        return math.inf
    return (1.0 + gamma) / (1.0 - gamma)


def vswr_to_s11_db(vswr: float) -> float:
    if vswr < 1.0:
        raise ValueError("linear VSWR cannot be below 1")
    gamma = (vswr - 1.0) / (vswr + 1.0)
    return 20.0 * math.log10(gamma) if gamma > 0 else -math.inf


def vswr_to_db(vswr: float) -> float:
    """Convert linear VSWR to dB(VSWR) = 20 log10(VSWR) as HFSS plots it."""
    return 20.0 * math.log10(vswr)


def vswr_db_to_linear(vswr_db: float) -> float:
    """Convert an HFSS dB(VSWR) reading back to linear VSWR."""
    return 10.0 ** (vswr_db / 20.0)


def load_hfss_csv(path: str | Path) -> tuple[list[float], list[float]]:
    """Return (freq_ghz, values) from a two-column HFSS CSV export."""
    freqs: list[float] = []
    vals: list[float] = []
    with open(path, newline="") as fh:
        reader = csv.reader(fh)
        next(reader)  # header
        for row in reader:
            if len(row) < 2:
                continue
            freqs.append(float(row[0]))
            vals.append(float(row[1]))
    return freqs, vals


@dataclass
class ResonanceSummary:
    f_res_ghz: float
    s11_min_db: float
    vswr: float
    f_low_ghz: float | None
    f_high_ghz: float | None

    @property
    def bandwidth_mhz(self) -> float | None:
        if self.f_low_ghz is None or self.f_high_ghz is None:
            return None
        return (self.f_high_ghz - self.f_low_ghz) * 1000.0

    @property
    def bandwidth_percent(self) -> float | None:
        if self.bandwidth_mhz is None:
            return None
        return self.bandwidth_mhz / 1000.0 / self.f_res_ghz * 100.0


def _interp_cross(x0: float, y0: float, x1: float, y1: float, level: float) -> float:
    return x0 + (level - y0) * (x1 - x0) / (y1 - y0)


def summarize_s11(freq_ghz: list[float], s11_db: list[float], level_db: float = -10.0) -> ResonanceSummary:
    """Find the deepest minimum and the contiguous band around it below ``level_db``."""
    if len(freq_ghz) != len(s11_db) or len(freq_ghz) < 3:
        raise ValueError("need matching freq / S11 arrays with at least 3 points")
    i_min = min(range(len(s11_db)), key=s11_db.__getitem__)
    f_low = f_high = None
    if s11_db[i_min] <= level_db:
        i = i_min
        while i > 0 and s11_db[i - 1] <= level_db:
            i -= 1
        if i > 0:
            f_low = _interp_cross(freq_ghz[i - 1], s11_db[i - 1], freq_ghz[i], s11_db[i], level_db)
        j = i_min
        while j < len(s11_db) - 1 and s11_db[j + 1] <= level_db:
            j += 1
        if j < len(s11_db) - 1:
            f_high = _interp_cross(freq_ghz[j], s11_db[j], freq_ghz[j + 1], s11_db[j + 1], level_db)
    return ResonanceSummary(freq_ghz[i_min], s11_db[i_min], s11_db_to_vswr(s11_db[i_min]), f_low, f_high)


def load_touchstone_s1p(path: str | Path) -> tuple[list[float], list[float]]:
    """Read a one-port Touchstone file and return (freq_ghz, S11 in dB).

    Handles the ``DB``, ``MA`` and ``RI`` data formats and Hz/kHz/MHz/GHz units.
    """
    scale = {"HZ": 1e-9, "KHZ": 1e-6, "MHZ": 1e-3, "GHZ": 1.0}
    unit, fmt = "GHZ", "MA"
    freqs: list[float] = []
    s11: list[float] = []
    with open(path) as fh:
        for raw in fh:
            line = raw.split("!")[0].strip()
            if not line:
                continue
            if line.startswith("#"):
                tokens = line[1:].upper().split()
                for t in tokens:
                    if t in scale:
                        unit = t
                    elif t in ("DB", "MA", "RI"):
                        fmt = t
                continue
            parts = line.split()
            f = float(parts[0]) * scale[unit]
            a, b = float(parts[1]), float(parts[2])
            if fmt == "DB":
                db = a
            elif fmt == "MA":
                db = 20.0 * math.log10(a) if a > 0 else -math.inf
            else:  # RI
                mag = math.hypot(a, b)
                db = 20.0 * math.log10(mag) if mag > 0 else -math.inf
            freqs.append(f)
            s11.append(db)
    return freqs, s11
