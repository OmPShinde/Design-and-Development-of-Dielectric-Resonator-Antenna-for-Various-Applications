# Prototype measurement log

## Setup (22 Sep 2026)

- Instrument: Anritsu ShockLine **MS46122B** vector network analyzer, one-port S11
- Sweep: about 5.30 to 6.00 GHz, IFBW 1 kHz
- DUT: zirconia cylinder (white) on an FR-4 board with a 3 mm microstrip feed, connector at the feed edge
- Photo: `results/measurements/vna_setup_zirconia_prototype.jpg` (screen shows the S11 *phase* trace with markers at 5.646, 5.804 and 5.702 GHz)
- Plot: `results/measurements/vna_s11_vswr_zirconia.jpg` (S11 and VSWR, exported and re-plotted)

## Results (read from the exported plot, so approximate)

| | Simulated | Measured |
|---|---|---|
| Resonance | 5.767 GHz | ≈ 5.70 GHz (−67 MHz, −1.2 %) |
| Minimum S11 | −50.25 dB | ≈ −28.8 dB |
| VSWR at resonance | 1.006 | ≈ 1.08 (consistent with −28.8 dB) |
| −10 dB band | 5.726-5.807 GHz (81 MHz) | roughly 5.65-5.80 GHz (rough read-off, confirm with raw data) |

The prototype resonates about 1 % below the simulated frequency and the null is shallower, which is typical when a prototype differs slightly from the model. Candidates to check: the actual ceramic permittivity and loss versus 23 and 0.0013, any air gap between the cylinder and the substrate or feed, cylinder dimensions, FR-4 tolerance, and SMA launch effects. These are hypotheses, not findings.

## Next steps

1. Export the raw trace as Touchstone (`.s1p`) into `results/measurements/` so curves can be overlaid with `python -m analysis.overlay_s11`.
2. Record the actual cylinder dimensions, ceramic grade/supplier and how it was attached.
3. Calibrate (SOLT) at the connector plane and note the calibration kit and date in this file.
4. Measure gain and radiation patterns in an anechoic chamber.
5. Re-simulate with measured dimensions and permittivity to see if the shift is explained.
