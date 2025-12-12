import argparse
from .fetcher import run_fetch
from .log_generator import run_generate
from .parser import read_and_parse_log
from .report import run_report


def main():
    parser = argparse.ArgumentParser(
        description="API'den veri çeker, sentetik log üretir ve logları analiz ederek rapor oluşturur."
    )
    parser.add_argument("--fetch", action="store_true",
                        help="API’den postları çek ve data/raw_posts.json dosyasını güncelle.")
    parser.add_argument("--generate", action="store_true",
                        help="data/raw_posts.json dosyasından data/app.log log dosyasını üret.")
    parser.add_argument("--analyze", action="store_true",
                        help="data/app.log dosyasını çözümle ve reports klasörüne raporları yaz.")

    args = parser.parse_args()

    if not (args.fetch or args.generate or args.analyze):
        print("Hata: En az bir argüman seçmelisin. Örnek: --fetch")
        return

    if args.fetch:
        run_fetch()
    if args.generate:
        run_generate()
    if args.analyze:
        records = read_and_parse_log()
        if records:
            run_report(records)
        else:
            print("Hata: Analiz edilecek geçerli log kaydı bulunamadı.")


if __name__ == "__main__":
    main()
