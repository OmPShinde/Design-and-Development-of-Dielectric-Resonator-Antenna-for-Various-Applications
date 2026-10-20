import json
import unittest
from pathlib import Path

from analysis import s11_tools as st

DATA = Path(__file__).resolve().parents[1] / "results" / "data" / "results_summary.json"


class ResultsData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = json.loads(DATA.read_text())

    def test_vswr_consistent_with_s11(self):
        for key in ("circular_patch", "alumina_cdra", "zirconia_cdra"):
            r = self.d["simulated"][key]
            self.assertAlmostEqual(st.s11_db_to_vswr(r["s11_min_db"]), r["vswr"], delta=0.01, msg=key)

    def test_bandwidth_consistent_with_band_edges(self):
        for key in ("circular_patch", "alumina_cdra", "zirconia_cdra"):
            r = self.d["simulated"][key]
            lo, hi = r["band_ghz"]
            self.assertAlmostEqual((hi - lo) * 1000, r["bandwidth_mhz"], delta=1.0, msg=key)
            self.assertAlmostEqual(r["bandwidth_mhz"] / 1000 / r["f_res_ghz"] * 100, r["bandwidth_percent"], delta=0.02, msg=key)

    def test_measured_vswr_consistent(self):
        m = self.d["measured"]["zirconia_cdra_vna"]
        self.assertAlmostEqual(st.s11_db_to_vswr(m["s11_min_db"]), m["vswr"], delta=0.01)


if __name__ == "__main__":
    unittest.main()
