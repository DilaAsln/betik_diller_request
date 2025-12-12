import json
from pathlib import Path
import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RAW_PATH = DATA_DIR / "raw_posts.json"

REQUIRED_KEYS = {"userId", "id", "title", "body"}


def fetch_posts(limit: int = 100) -> list[dict]:
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        print("Hata: API isteği zaman aşımına uğradı.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Hata: API isteği başarısız: {e}")
        return []
    except ValueError:
        print("Hata: JSON verisi çözümlenemedi.")
        return []

    # JSON doğrulama
    if not isinstance(data, list):
        print("Hata: Beklenen JSON formatı liste değil.")
        return []
    data = data[:limit]
    for i, item in enumerate(data):
        if not isinstance(item, dict) or not REQUIRED_KEYS.issubset(item.keys()):
            print(f"Hata: {i}. kayıt beklenen alanları içermiyor.")
            return []

    return data


def run_fetch() -> None:
    posts = fetch_posts()

    # İnternet/DNS yoksa: ödevin geri kalanını çalıştırmak için offline veri
    if not posts:
        print("Uyarı: API erişilemedi (DNS/Internet). Offline 100 kayıt üretildi.")
        posts = [
            {"userId": (i % 10) + 1, "id": i, "title": f"offline title {i}", "body": f"offline body {i}"}
            for i in range(1, 101)
        ]

    DATA_DIR.mkdir(exist_ok=True)
    with RAW_PATH.open("w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

    print(f"{len(posts)} post kaydedildi → data/raw_posts.json")
