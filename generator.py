"""Güvenli şifre üretici — `secrets` modülü tabanlı (kriptografik RNG).

Dikkat: `random` modülü Mersenne Twister kullanır ve tahmin edilebilir
olduğundan güvenlik amaçlı KULLANILMAZ; burada yalnızca `secrets` var.
"""

import secrets
import string

SEMBOLLER = "!@#$%^&*()-_=+[]{}?<>"
KELIME_LISTESI_URL = "https://www.eff.org/dice"  # ciddi kullanım için büyük liste

# Parola üretimi için demo kelime listesi (ciddi kullanım için EFF Diceware önerilir)
KELIMELER = [
    "kalem", "kitap", "deniz", "yıldız", "orman", "dag", "nehir", "kus",
    "kelebek", "seker", "kahve", "cay", "limon", "elma", "armut", "kiraz",
    "uzum", "karpuz", "peynir", "ekmek", "balik", "kedi", "kopek", "aslan",
    "kaplan", "kurt", "ayi", "tilki", "tavsan", "sincap", "baykus", "kartal",
    "marti", "keci", "inek", "koyun", "tavuk", "ari", "karinca", "capul",
    "rüzgar", "bulut", "yagmur", "kar", "gunes", "ay", "gokyuzu", "toprak",
    "tas", "cicek", "agac", "yaprak", "kok", "tohum", "bahce", "orman",
    "cali", "cayir", "gol", "dere", "selale", "magara", "tepe", "vadi",
    "ada", "kiyi", "liman", "gemi", "yelken", "dur", "kacis", "siginak",
]


def _karistir(karakterler: list) -> None:
    """Fisher-Yates karıştırma — `secrets` tabanlı."""
    for i in range(len(karakterler) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        karakterler[i], karakterler[j] = karakterler[j], karakterler[i]


def sifre_uret(uzunluk: int = 16, buyuk_harf: bool = True,
               rakam: bool = True, sembol: bool = True) -> str:
    """Her seçili karakter sınıfından en az bir karakter içeren güvenli şifre üretir."""
    if uzunluk < 4:
        raise ValueError("Uzunluk en az 4 olmalı.")

    siniflar = [string.ascii_lowercase]
    if buyuk_harf:
        siniflar.append(string.ascii_uppercase)
    if rakam:
        siniflar.append(string.digits)
    if sembol:
        siniflar.append(SEMBOLLER)

    # Her sınıftan en az bir karakter garanti et, kalanını havuzdan doldur
    karakterler = [secrets.choice(sinif) for sinif in siniflar]
    havuz = "".join(siniflar)
    karakterler += [secrets.choice(havuz) for _ in range(uzunluk - len(karakterler))]
    _karistir(karakterler)
    return "".join(karakterler)


def parola_uret(kelime_sayisi: int = 5, ayirici: str = "-",
                buyuk_harf: bool = True, rakam: bool = True) -> str:
    """Hatırlanabilir parola üretir: rastgele kelimeler + isteğe bağlı sayı."""
    if kelime_sayisi < 3:
        raise ValueError("Kelime sayısı en az 3 olmalı.")

    kelimeler = [secrets.choice(KELIMELER) for _ in range(kelime_sayisi)]
    if buyuk_harf:
        i = secrets.randbelow(kelime_sayisi)
        kelimeler[i] = kelimeler[i].capitalize()
    if rakam:
        kelimeler.append(str(secrets.randbelow(90) + 10))  # 10-99 arası sayı
    return ayirici.join(kelimeler)
