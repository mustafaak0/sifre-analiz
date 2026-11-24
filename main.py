"""SifreAnaliz — şifre güçlülük analizi ve güvenli şifre üretimi (CLI)."""

import argparse
import getpass

from analyzer import analiz_et
from generator import parola_uret, sifre_uret


def _analiz_yazdir(sifre: str) -> None:
    r = analiz_et(sifre)
    print(f"Uzunluk:       {r['uzunluk']} karakter (alfabe: {r['havuz']} simge)")
    print(f"Entropy:       {r['entropy']} bit")
    print(f"Kategori:      {r['kategori']}")
    print(f"Yaygın şifre:  {'EVET — hemen değiştirin!' if r['yaygin'] else 'hayır'}")
    print(f"Ardışık desen: {'var (abc, 123 gibi)' if r['ardisik_desen'] else 'yok'}")
    print(f"Tekrar:        {'var (aaa, 111 gibi)' if r['tekrar_desen'] else 'yok'}")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="sifre-analiz",
        description="Şifre güçlülük analizi ve kriptografik güvenli şifre üretici",
    )
    alt = parser.add_subparsers(dest="komut", required=True)

    analiz_p = alt.add_parser("analiz", help="Bir şifrenin güçlülüğünü analiz et")
    analiz_p.add_argument(
        "sifre",
        help="Analiz edilecek şifre ('-' verirsen gizli olarak sorulur)",
    )

    uret_p = alt.add_parser("uret", help="Güvenli şifre üret")
    uret_p.add_argument("-n", "--uzunluk", type=int, default=16,
                        help="Şifre uzunluğu (varsayılan: 16)")
    uret_p.add_argument("--sembol-yok", action="store_true",
                        help="Sembolleri hariç tut")
    uret_p.add_argument("--parola", action="store_true",
                        help="Hatırlanabilir parola üret (rastgele kelimeler)")
    uret_p.add_argument("-k", "--kelime", type=int, default=5,
                        help="Parola modunda kelime sayısı (varsayılan: 5)")

    args = parser.parse_args()

    if args.komut == "analiz":
        sifre = getpass.getpass("Şifre: ") if args.sifre == "-" else args.sifre
        _analiz_yazdir(sifre)
    elif args.komut == "uret":
        if args.parola:
            print(parola_uret(kelime_sayisi=args.kelime))
        else:
            print(sifre_uret(uzunluk=args.uzunluk, sembol=not args.sembol_yok))


if __name__ == "__main__":
    main()
