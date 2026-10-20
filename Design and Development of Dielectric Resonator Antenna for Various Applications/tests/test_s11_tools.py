import math
import tempfile
from pathlib import Path
import unittest

from analysis import s11_tools as st


class Conversions(unittest.TestCase):
    def test_zirconia_vswr_matches_paper(self):
        v = st.s11_db_to_vswr(-50.25)
        self.assertAlmostEqual(v, 1.006, places=3)
        # the HFSS plot marker of 0.0534 is dB(VSWR), not linear VSWR
        self.assertAlmostEqual(st.vswr_to_db(v), 0.0534, places=3)
        self.assertAlmostEqual(st.vswr_db_to_linear(0.0534), 1.006, places=3)

    def test_other_designs(self):
        self.assertAlmostEqual(st.s11_db_to_vswr(-25.07), 1.12, places=2)
        self.assertAlmostEqual(st.s11_db_to_vswr(-15.95), 1.38, places=2)

    def test_measured_zirconia(self):
        self.assertAlmostEqual(st.s11_db_to_vswr(-28.8), 1.08, places=2)

    def test_roundtrip(self):
        self.assertAlmostEqual(st.vswr_to_s11_db(st.s11_db_to_vswr(-17.3)), -17.3, places=6)

    def test_vswr_below_one_rejected(self):
        with self.assertRaises(ValueError):
            st.vswr_to_s11_db(0.9)


class Summary(unittest.TestCase):
    def _synthetic(self):
        f = [5.0 + 0.001 * i for i in range(1001)]
        s = [-4.0 - 46.0 / (1 + ((x - 5.767) / 0.012) ** 2) for x in f]
        return f, s

    def test_summarize_finds_resonance_and_band(self):
        f, s = self._synthetic()
        r = st.summarize_s11(f, s)
        self.assertAlmostEqual(r.f_res_ghz, 5.767, places=3)
        self.assertLess(r.s11_min_db, -49)
        self.assertIsNotNone(r.bandwidth_mhz)
        # analytic -10 dB width of the Lorentzian: 2*0.012*sqrt(46/6 - 1) GHz ~= 62 MHz
        self.assertAlmostEqual(r.bandwidth_mhz, 62.0, delta=1.0)

    def test_no_band_when_never_below_level(self):
        f = [5.0, 5.5, 6.0]
        r = st.summarize_s11(f, [-3, -5, -4])
        self.assertIsNone(r.bandwidth_mhz)


if __name__ == "__main__":
    unittest.main()


class Touchstone(unittest.TestCase):
    def _write(self, tmp, text):
        p = Path(tmp) / "x.s1p"
        p.write_text(text)
        return p

    def test_db_format(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(d, "! c\n# GHz S DB R 50\n5.7 -28.8 -100\n5.8 -10.0 20\n")
            f, s = st.load_touchstone_s1p(p)
            self.assertEqual(f, [5.7, 5.8])
            self.assertEqual(s, [-28.8, -10.0])

    def test_ma_and_hz_units(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(d, "# HZ S MA R 50\n5700000000 0.1 30\n")
            f, s = st.load_touchstone_s1p(p)
            self.assertAlmostEqual(f[0], 5.7)
            self.assertAlmostEqual(s[0], -20.0, places=6)

    def test_ri_format(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(d, "# GHZ S RI R 50\n5.7 0.03 0.04\n")
            _, s = st.load_touchstone_s1p(p)
            self.assertAlmostEqual(s[0], 20 * math.log10(0.05), places=6)
