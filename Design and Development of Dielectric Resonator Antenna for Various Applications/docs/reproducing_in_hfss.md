# Reproducing the results in HFSS

## 1. Zirconia CDRA (proposed design)

1. Open `hfss/zirconia_cdra/zirconia_cdra_5p8GHz.aedt`.
2. Check materials: Zirconia εr 23. The file has tan δ 0.0013; the paper states 0.002, so decide which to use and note it.
3. Confirm geometry against `results/figures/zirconia_cdra/cad_dimensions.png`: 60 × 60 × 1.6 mm FR-4, Ø12.4 × 10 mm cylinder centred on the board, 3 mm feed from the board edge to the cylinder rim.
4. **Analyze** Setup1 (adaptive frequency, 5-6 GHz sweep).
5. Create reports: S11 (`dB(S(1,1))`), VSWR (`VSWR(1)`, linear), `dB(PeakRealizedGain)`, `RadiationEfficiency`, 3D polar `dB(DirTotal)`, and 2D patterns at φ = 0° and 90°.
6. Expect a resonance near 5.767 GHz with S11 ≈ −50 dB.

## 2. Alumina CDRA

Same board and feed. Ø42.4 × 15 mm cylinder, εr 9.9. Sweep 5.2-6 GHz. Expect S11 ≈ −25 dB at 5.769 GHz and a boresight null with lobes tilted about 40-60° off axis.

## 3. Circular patch

27 × 24 × 1.6 mm FR-4, patch radius 6.7 mm, 3 mm feed with 0.5 mm × 8 mm inset slots on each side. Expect S11 ≈ −15.95 dB at 5.827 GHz.

Patch radius from the cavity model: `python -m analysis.design_calcs` (gives 6.83 mm; the optimised design uses 6.7 mm).

## 4. Parasitic-ring design

Extend the sweep to 1-9 GHz. The central zirconia cylinder (radius 8.3, height 12) sits inside a 12-sided zirconia ring (inner radius 12, circumradius 15, height 12), leaving a 3.7 mm gap; the 35 mm feed passes under the ring. Expect matches near 4.05, 5.02, 5.84 and 8.20 GHz.

## Exporting results

Export each report as CSV into `results/data/` (see its README), then:

```bash
python -m analysis.compare_results
python -m analysis.overlay_s11 --sim ... --meas ... --out ...
```
