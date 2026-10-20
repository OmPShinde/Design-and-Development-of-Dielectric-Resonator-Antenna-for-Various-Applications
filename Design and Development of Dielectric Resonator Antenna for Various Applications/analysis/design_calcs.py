"""Design equations and derived quantities used in the paper.

Run ``python -m analysis.design_calcs`` to print every number that the paper
derives analytically (patch radius, size-scaling ratio, volumes, electrical
size, ceramic mass) so they can be checked against the text.

Equation numbers refer to Zirconia_DRA_for_5_8_GHz.docx.
"""
from __future__ import annotations

import math

C0_MM_GHZ = 299.792458  # speed of light in mm * GHz  (c = 299 792 458 m/s)


def free_space_wavelength_mm(f_ghz: float) -> float:
    """lambda_0 in mm for a frequency in GHz."""
    return C0_MM_GHZ / f_ghz


def cdra_radius_scale(er_ref: float, er_new: float) -> float:
    """Eq. (2): ratio a_new / a_ref at a fixed frequency.

    From Eq. (1), f_r ~ 1 / (a * sqrt(er + 2)) for a cylindrical DR of fixed
    aspect ratio, so a ~ 1 / sqrt(er + 2).
    """
    return math.sqrt((er_ref + 2.0) / (er_new + 2.0))


def cylinder_volume_mm3(radius_mm: float, height_mm: float) -> float:
    return math.pi * radius_mm**2 * height_mm


def cylinder_footprint_mm2(radius_mm: float) -> float:
    return math.pi * radius_mm**2


def reduction_percent(new: float, ref: float) -> float:
    """Percentage by which ``new`` is smaller than ``ref``."""
    return (1.0 - new / ref) * 100.0


def cylinder_mass_g(volume_mm3: float, density_g_cm3: float) -> float:
    return volume_mm3 / 1000.0 * density_g_cm3


def circular_patch_radius_mm(fr_ghz: float, er: float, h_mm: float) -> float:
    """Eqs. (3)-(4): cavity-model radius of a circular patch (Balanis).

    F and h are in centimetres inside the formula.
    """
    h_cm = h_mm / 10.0
    f_hz = fr_ghz * 1e9
    F = 8.791e9 / (f_hz * math.sqrt(er))
    a_cm = F / math.sqrt(
        1.0 + (2.0 * h_cm) / (math.pi * er * F)
        * (math.log(math.pi * F / (2.0 * h_cm)) + 1.7726)
    )
    return a_cm * 10.0


def fractional_bandwidth_percent(f_low_ghz: float, f_high_ghz: float, f_center_ghz: float | None = None) -> float:
    fc = f_center_ghz if f_center_ghz is not None else 0.5 * (f_low_ghz + f_high_ghz)
    return (f_high_ghz - f_low_ghz) / fc * 100.0


def main() -> None:
    f_zr, f_al = 5.767, 5.769
    lam_zr = free_space_wavelength_mm(f_zr)
    lam_al = free_space_wavelength_mm(f_al)

    print("== Size scaling (Eq. 2) ==")
    ratio = cdra_radius_scale(9.9, 23.0)
    print(f"a_Zr / a_Al = {ratio:.3f}   volume ratio = {ratio**3:.3f}")

    print("\n== Resonator volumes ==")
    v_zr = cylinder_volume_mm3(6.2, 10.0)
    v_al = cylinder_volume_mm3(21.2, 15.0)
    v_hasan = cylinder_volume_mm3(10.0, 10.0)  # ref [12]: D20 x 10
    print(f"Zirconia  (r=6.2,  h=10): {v_zr:9.0f} mm^3")
    print(f"Alumina   (r=21.2, h=15): {v_al:9.0f} mm^3")
    print(f"Volume saving vs own-board alumina: {reduction_percent(v_zr, v_al):.1f} %")
    print(f"Footprint saving vs ref [12] (D20): "
          f"{reduction_percent(cylinder_footprint_mm2(6.2), cylinder_footprint_mm2(10.0)):.1f} %")
    print(f"Height saving vs own-board alumina: {reduction_percent(10, 15):.0f} %")

    print("\n== Electrical size ==")
    print(f"lambda0 @ {f_zr} GHz = {lam_zr:.1f} mm; "
          f"D/lambda0 = {12.4 / lam_zr:.2f}, h/lambda0 = {10 / lam_zr:.2f}")
    print(f"Alumina D/lambda0 @ {f_al} GHz = {42.4 / lam_al:.2f}")

    print("\n== Ceramic mass (densities within the Table I ranges; the paper's 7.3 g implies ~6.05 g/cm^3) ==")
    print(f"Zirconia   ({v_zr:.0f} mm^3 x 6.05 g/cm^3): {cylinder_mass_g(v_zr, 6.05):.1f} g")
    print(f"Alumina    ({v_al:.0f} mm^3 x 3.9 g/cm^3): {cylinder_mass_g(v_al, 3.9):.1f} g")
    print(f"Alumina D20x10 ref [12]       : {cylinder_mass_g(v_hasan, 3.9):.1f} g")

    print("\n== Reference circular patch (Eqs. 3-4) ==")
    a = circular_patch_radius_mm(5.8, 4.4, 1.6)
    print(f"Calculated radius a = {a:.2f} mm (simulated design uses 6.7 mm)")


if __name__ == "__main__":
    main()
