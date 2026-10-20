# HFSS models

Created with Ansys Electronics Desktop (HFSS). Open the `.aedt` file, then **Project Manager → Analysis → Setup1 → Analyze**.

| Model | File | Resonator | Sweep stored in file | Adaptive solution |
|---|---|---|---|---|
| Circular patch | `circular_patch/circular_patch_5p8GHz.aedt` | Cu patch, `patch_rad` = 6.7 mm | 5-6 GHz | 5.8 GHz, 20 passes, ΔS 0.02 |
| Alumina CDRA | `alumina_cdra/alumina_cdra_5p8GHz.aedt` | Ø42.4 × 15 mm, εr 9.9 | 5.2-6 GHz | 5.8 GHz, 20 passes, ΔS 0.02 |
| Zirconia CDRA | `zirconia_cdra/zirconia_cdra_5p8GHz.aedt` | Ø12.4 × 10 mm, εr 23 | 5-6 GHz | 5 GHz, 6 passes, ΔS 0.02 |
| Zirconia + ring | `zirconia_parasitic_ring/zirconia_parasitic_ring_multiband.aedt` | Ø16.6 × 12 mm cylinder + 12-sided ring | 2-7 GHz (plots cover 1-9 GHz) | 16 passes |

## Common set-up

- Substrate FR-4, εr 4.4, tan δ 0.02, thickness `SH` = 1.6 mm, ground plane on the bottom face (Perfect E)
- 3 mm microstrip feed (`MW`), **wave port**, one mode, from the board edge
- Radiation boundary around an air region
- Materials in every file: FR-4, Rogers RT/duroid 5880, "Alumina Ceamic" (sic; εr 9.9, tan δ 0.0001), and a project-level **Zirconia** (εr 23, tan δ 0.0013)

> The loss tangents stored here differ from those quoted in the paper (0.002). See [../docs/KNOWN_ISSUES.md](../docs/KNOWN_ISSUES.md).

## Design variables

Zirconia CDRA (`SL` 60, `SW` 60, `SH` 1.6, `MW` 3), cylinder Ø12.4 × 10 mm.

Circular patch (screenshot: `results/figures/circular_patch/hfss_parameters.jpeg`):

| SL | SW | SH | MW | M | L | rad | h | patch_rad |
|---|---|---|---|---|---|---|---|---|
| 27 | 24 | 1.6 | 3 | 3 | 6.3 | 10 | 10 | 6.7 |

Zirconia + ring (screenshot: `results/figures/zirconia_parasitic_ring/hfss_parameters.jpeg`):

| SL | SW | SH | MW | M | L | rad | h | RC |
|---|---|---|---|---|---|---|---|---|
| 60 | 60 | 1.6 | 3 | 3 | 35 | 12 | 12 | 8.3 |

`RC` = centre cylinder radius, `rad` = ring inner radius (12-sided ring, 15 mm circumradius, 28.98 mm across flats), `h` = height of both, `L` = feed length.

## Notes

- `.aedt` files are plain text and diff reasonably in git. Do not commit the `*.aedtresults/` folders (they are in `.gitignore`).
- Files were saved by one Electronics Desktop version; open in the same or a newer release.
