import math
import unittest

from analysis import design_calcs as dc


class DesignCalcs(unittest.TestCase):
    def test_radius_scale_matches_paper(self):
        self.assertAlmostEqual(dc.cdra_radius_scale(9.9, 23.0), 0.69, places=2)

    def test_volumes_match_table_ii(self):
        self.assertAlmostEqual(dc.cylinder_volume_mm3(6.2, 10), 1208, delta=1)
        self.assertAlmostEqual(dc.cylinder_volume_mm3(21.2, 15), 21179, delta=1)

    def test_reductions_match_paper(self):
        v_zr, v_al = dc.cylinder_volume_mm3(6.2, 10), dc.cylinder_volume_mm3(21.2, 15)
        self.assertAlmostEqual(dc.reduction_percent(v_zr, v_al), 94.3, places=1)
        fp = dc.reduction_percent(dc.cylinder_footprint_mm2(6.2), dc.cylinder_footprint_mm2(10.0))
        self.assertAlmostEqual(fp, 61.6, places=1)

    def test_electrical_size(self):
        lam = dc.free_space_wavelength_mm(5.767)
        self.assertAlmostEqual(lam, 52.0, delta=0.1)
        self.assertAlmostEqual(12.4 / lam, 0.24, places=2)
        self.assertAlmostEqual(10 / lam, 0.19, places=2)

    def test_masses(self):
        self.assertAlmostEqual(dc.cylinder_mass_g(1208, 6.05), 7.3, delta=0.1)
        self.assertAlmostEqual(dc.cylinder_mass_g(21179, 3.9), 83, delta=1)

    def test_patch_radius(self):
        self.assertAlmostEqual(dc.circular_patch_radius_mm(5.8, 4.4, 1.6), 6.8, delta=0.1)

    def test_fractional_bandwidth(self):
        self.assertAlmostEqual(dc.fractional_bandwidth_percent(5.726, 5.807, 5.767), 1.40, delta=0.02)


if __name__ == "__main__":
    unittest.main()
