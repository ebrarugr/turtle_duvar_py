"""ROS 2 kurulumu olmadan da çalıştırılabilen mantık testleri."""

import math
import unittest

from turtle_duvar_py.hareket_mantigi import aciyi_normalize_et, yeni_yon_hesapla


class HareketMantigiTest(unittest.TestCase):
    def test_ortada_duvar_yok(self):
        self.assertIsNone(yeni_yon_hesapla(5, 5, 0, 1, 10))

    def test_sag_duvarda_geri_don(self):
        self.assertAlmostEqual(abs(yeni_yon_hesapla(10, 5, 0, 1, 10)), math.pi)

    def test_sol_duvarda_geri_don(self):
        self.assertAlmostEqual(yeni_yon_hesapla(1, 5, math.pi, 1, 10), 0)

    def test_ust_duvarda_yansi(self):
        self.assertAlmostEqual(yeni_yon_hesapla(5, 10, math.pi / 4, 1, 10), -math.pi / 4)

    def test_kosede_iki_duvardan_yansi(self):
        self.assertAlmostEqual(yeni_yon_hesapla(10, 10, math.pi / 4, 1, 10), -3 * math.pi / 4)

    def test_iceriyi_gosteriyorsa_ayni_duvarda_tekrar_donmez(self):
        self.assertIsNone(yeni_yon_hesapla(10, 5, math.pi, 1, 10))

    def test_aci_normalizasyonu(self):
        self.assertAlmostEqual(aciyi_normalize_et(3 * math.pi / 2), -math.pi / 2)


if __name__ == '__main__':
    unittest.main()
