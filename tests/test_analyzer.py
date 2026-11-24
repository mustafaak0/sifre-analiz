"""analyzer ve generator birim testleri."""

import math
import unittest

from analyzer import analiz_et, entropy, havuz_boyutu
from generator import parola_uret, sifre_uret


class TestEntropy(unittest.TestCase):
    def test_bos_sifre(self):
        self.assertEqual(entropy(""), 0.0)

    def test_tek_karakter_sinifi(self):
        # 8 haneli hepsi küçük harf: 8 * log2(26) ≈ 37.6
        self.assertAlmostEqual(entropy("abcdefgh"), 8 * math.log2(26), places=2)

    def test_havuz_boyutu(self):
        self.assertEqual(havuz_boyutu("abc"), 26)
        self.assertEqual(havuz_boyutu("aB3!"), 26 + 26 + 10 + 33)


class TestAnaliz(unittest.TestCase):
    def test_yaygin_sifre_cok_zayif(self):
        r = analiz_et("123456")
        self.assertTrue(r["yaygin"])
        self.assertEqual(r["kategori"], "Çok Zayıf")

    def test_yaygin_sifre_uzun_olsa_da_zayif(self):
        r = analiz_et("passwordpassword")
        self.assertTrue(r["yaygin"])
        self.assertEqual(r["kategori"], "Çok Zayıf")

    def test_ardisik_desen(self):
        self.assertTrue(analiz_et("Klavye123abc")["ardisik_desen"])

    def test_tekrar_deseni(self):
        self.assertTrue(analiz_et("aaa123xyz")["tekrar_desen"])

    def test_kisa_sifre_sinirlandirilir(self):
        r = analiz_et("aB3!")
        self.assertEqual(r["kategori"], "Çok Zayıf")

    def test_guclu_sifre(self):
        r = analiz_et("T3k!Rast#Sifre+2026")
        self.assertIn(r["kategori"], ("Güçlü", "Çok Güçlü"))
        self.assertFalse(r["yaygin"])


class TestUretici(unittest.TestCase):
    def test_uzunluk(self):
        self.assertEqual(len(sifre_uret(20)), 20)

    def test_sinif_garantisi(self):
        s = sifre_uret(12)
        self.assertTrue(any(c.islower() for c in s))
        self.assertTrue(any(c.isupper() for c in s))
        self.assertTrue(any(c.isdigit() for c in s))
        self.assertTrue(any(not c.isalnum() for c in s))

    def test_sembolsiz(self):
        s = sifre_uret(16, sembol=False)
        self.assertTrue(s.isalnum())

    def test_kisa_uzunluk_reddedilir(self):
        with self.assertRaises(ValueError):
            sifre_uret(3)

    def test_parola_kelime_sayisi(self):
        p = parola_uret(kelime_sayisi=4, rakam=False)
        self.assertEqual(len(p.split("-")), 4)

    def test_parola_rakam_ekler(self):
        p = parola_uret(kelime_sayisi=4, rakam=True)
        self.assertTrue(p.split("-")[-1].isdigit())


if __name__ == "__main__":
    unittest.main()
