# sifre-analiz

Şifre güçlülük analizi ve kriptografik olarak güvenli şifre üretici.
Saf Python (standart kütüphane) — **bağımlılık yok**.

## Özellikler

- **Entropy tabanlı skorlama** — brute-force maliyetine göre Çok Zayıf → Çok Güçlü kategorisi
- **Yaygın şifre tespiti** — sızma listelerinden derlenmiş sözlük kontrolü
- **Desen tespiti** — ardışık diziler (`abc`, `123`) ve tekrarlar (`aaa`, `111`)
- **Güvenli üretim** — `secrets` modülü (kriptografik RNG), `random` asla kullanılmaz
- **Parola modu** — hatırlanabilir rastgele kelimelerden parola üretimi
- **Birim testler** — `unittest` ile

## Kurulum

Python 3.10+ yeterlidir, ek kurulum gerektirmez:

```bash
git clone https://github.com/mustafaak0/sifre-analiz.git
cd sifre-analiz
```

## Kullanım

Şifre analizi:

```bash
python main.py analiz "sifreniz"
# Shell geçmişine düşmesin istersen:
python main.py analiz -
```

Güvenli şifre üret:

```bash
python main.py uret                 # 16 karakter, tüm sınıflar
python main.py uret -n 24           # 24 karakter
python main.py uret --sembol-yok    # sembolsüz
python main.py uret --parola -k 6   # 6 kelimelik hatırlanabilir parola
```

Örnek çıktı:

```
Uzunluk:       19 karakter (alfabe: 95 simge)
Entropy:       124.8 bit
Kategori:      Güçlü
Yaygın şifre:  hayır
Ardışık desen: yok
Tekrar:        yok
```

## Testler

```bash
python -m unittest discover -s tests -v
```

## Güvenlik notları

- CLI'a düz yazdığınız şifre **shell geçmişine düşer** — `analiz -` kullanıp gizli giriş yapın.
- Bu araç **offline** çalışır; şifreniz hiçbir yere gönderilmez.
- Entropy hesabı yaklaşıktır (Türkçe karakterler ASCII alfabesine yakın hesaplanır);
  zxcvbn gibi gelişmiş modeller kadar kapsamlı değildir.
- Üretilen parolalar için gömülü kelime listesi küçüktür; ciddi kullanımda
  [EFF Diceware](https://www.eff.org/dice) listesi ve 6+ kelime önerilir.
- Hiçbir zaman aynı şifreyi ikinci kez kullanmayın; bir parola yöneticisi edinin.

## Lisans

Henüz lisans eklenmedi. Gerekirse MIT, Apache-2.0 vb. eklenebilir.
