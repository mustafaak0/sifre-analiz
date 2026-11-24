"""Şifre güçlülük analizi — entropy, yaygın şifre ve desen tespiti."""

import math
import string

# Sık kullanılan şifrelerden derlenmiş küçük bir liste (sızma listelerinden örneklendirilmiştir)
YAYGIN_SIFRELER = {
    "123456", "password", "123456789", "12345678", "12345", "qwerty",
    "111111", "1234567", "dragon", "123123", "abc123", "iloveyou",
    "admin", "welcome", "monkey", "login", "princess", "qwerty123",
    "solo", "passw0rd", "starwars", "master", "hello", "freedom",
    "whatever", "qazwsx", "trustno1", "batman", "letmein", "654321",
    "sifre", "sifre123", "mustafa", "turkiye", "istanbul", "ankara",
}

# (üst eşik, kategori) — entropy bit cinsinden skorlanır
KATEGORILER = [
    (28, "Çok Zayıf"),
    (36, "Zayıf"),
    (60, "Orta"),
    (128, "Güçlü"),
]

SEMBOL_ADET = 33  # klavyedeki yaygın yazdırılabilir semboller


def havuz_boyutu(sifre: str) -> int:
    """Şifredeki karakterlerin olası alfabesinin büyüklüğü (yaklaşık)."""
    havuz = 0
    if any(c.islower() for c in sifre):
        havuz += 26
    if any(c.isupper() for c in sifre):
        havuz += 26
    if any(c.isdigit() for c in sifre):
        havuz += 10
    if any(not c.isalnum() for c in sifre):
        havuz += SEMBOL_ADET
    return havuz


def entropy(sifre: str) -> float:
    """Brute-force maliyetinin log2 tabanında yaklaşık ölçüsü (bit)."""
    havuz = havuz_boyutu(sifre)
    if not sifre or havuz <= 1:
        return 0.0
    return len(sifre) * math.log2(havuz)


def _ardisik_desen_var_mi(sifre: str) -> bool:
    """'abc', '321' gibi 3+ ardışık karakter dizisi arar."""
    for i in range(len(sifre) - 2):
        a, b, c = ord(sifre[i]), ord(sifre[i + 1]), ord(sifre[i + 2])
        if (b - a == 1 and c - b == 1) or (a - b == 1 and b - c == 1):
            return True
    return False


def _tekrar_deseni_var_mi(sifre: str) -> bool:
    """'aaa', '111' gibi 3+ tekrarlanan karakter arar."""
    for i in range(len(sifre) - 2):
        if sifre[i] == sifre[i + 1] == sifre[i + 2]:
            return True
    return False


def _kategori(puan: float) -> str:
    for esik, ad in KATEGORILER:
        if puan < esik:
            return ad
    return "Çok Güçlü"


def _yaygin_mi(sifre: str) -> bool:
    """Tam eşik veya 6+ karakterli yaygın bir şifrenin geçmesi (passwordpassword gibi)."""
    kucuk = sifre.lower()
    if kucuk in YAYGIN_SIFRELER:
        return True
    return any(ys in kucuk for ys in YAYGIN_SIFRELER if len(ys) >= 6)


def analiz_et(sifre: str) -> dict:
    """Şifreyi analiz eder; metrikler, skor (bit) ve kategori döndürür."""
    yaygin = _yaygin_mi(sifre)
    ardisik = _ardisik_desen_var_mi(sifre)
    tekrar = _tekrar_deseni_var_mi(sifre)

    puan = entropy(sifre)
    if yaygin:
        puan = min(puan, 10)  # yaygın şifre ne kadar uzun olursa olsun zayıftır
    else:
        if ardisik:
            puan *= 0.75
        if tekrar:
            puan *= 0.75
        if len(sifre) < 8:
            puan = min(puan, 20)

    return {
        "uzunluk": len(sifre),
        "havuz": havuz_boyutu(sifre),
        "entropy": round(puan, 1),
        "kategori": _kategori(puan),
        "yaygin": yaygin,
        "ardisik_desen": ardisik,
        "tekrar_desen": tekrar,
    }
