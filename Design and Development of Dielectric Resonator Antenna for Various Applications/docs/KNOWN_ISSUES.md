# Known inconsistencies between sources

Found while assembling this repository. The **paper** (`docs/paper`) is treated as authoritative for all reported numbers; the other sources are listed so they can be corrected.

## 1. Loss tangents: HFSS files vs paper vs slides

| Material | HFSS `.aedt` files | Paper (Sec. II-B, Table I) | Slides (slides 7, 15) |
|---|---|---|---|
| Alumina | **0.0001** (library material "Alumina Ceamic") | 0.002 | 0.001 |
| Zirconia | **0.0013** | 0.002 | 0.001 |
| FR-4 | 0.02 | 0.02 | n/a |

The simulations as saved use lower loss than the paper states. Efficiency figures could therefore change when the models are re-run with 0.002. **Action:** decide which values are correct, then fix the paper or the models and re-export.

## 2. Alumina permittivity

Paper and HFSS file: εr = 9.9. Slides 7, 8 and 24: εr = 9.8.

## 3. Slide summary tables vs paper Table III

| Quantity | Slides | Paper |
|---|---|---|
| Alumina peak realized gain | 5.40 dB | 5.2 dBi (4.7 dBi at fr) |
| Alumina radiation efficiency | 72 % | 68.5 % at fr |
| Alumina VSWR | 1.2 | 1.12 |
| Patch peak gain | 3.80 dB | 3.7 dBi |
| Zirconia peak gain | 7.75 dB | 7.85 dBi (5.9 dBi at fr) |
| Zirconia radiation efficiency | 88 % | 85.6 % at fr |
| Zirconia VSWR | **0.1** | 1.006 (the 0.0534 on the HFSS plot is **dB**(VSWR), not linear) |

## 4. Size-scaling claim in the slides

Slide 15 says zirconia εr ≈ 23 is "3.06×" alumina and that linear size shrinks 1.75×; slide 24 says ≈ 0.57×. Those ratios correspond to εr ≈ 30 (30 / 9.8 = 3.06, √3.06 = 1.75), not the εr = 23 simulated. The paper's Eq. (2), √((9.9+2)/(23+2)), gives **0.69** (volume ≈ 0.33).

## 5. Leftovers from an earlier 2.4 GHz study in the slides

- Slide 11 contains the stray text "Q1: Metal Patch vs Alumina CDRA at 2.40 GHz".
- Slide 24 says the patch resonated at 2.4 GHz with −11.76 dB and +2.5 dB gain, which contradicts the 5.8 GHz patch results (−15.95 dB at 5.827 GHz, 3.7 dBi).
- Slide 5 mentions the 2.4 GHz ISM band; the project targets 5.8 GHz.

## 6. Patch drawing variant

`results/figures/circular_patch/cad_dimensions_rad10_earlier_variant.png` shows a Ø20 mm patch (`rad = 10` in the HFSS variable table). The design reported in the paper uses `patch_rad = 6.7` mm (Ø13.4), shown in `cad_dimensions.png`. The HFSS patch file still contains both variables.

## 7. Parasitic-ring sweep range

The sweep stored in `zirconia_parasitic_ring_multiband.aedt` spans 2-7 GHz, while the published S11, gain and efficiency plots cover 1-9 GHz. The model was probably re-swept before plotting; extend the sweep to reproduce the 8.2 GHz band.

## 8. Zirconia VSWR plot

`results/figures/zirconia_cdra/vswr_dB_labelled.jpeg` is labelled dB(VSWR(1)) with a marker of 0.0534. Convert with `analysis.s11_tools.vswr_db_to_linear` (gives 1.006) or re-plot linear VSWR before using it in a figure.
