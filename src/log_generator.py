import json
import random
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
RAW_PATH = DATA_DIR / "raw_posts.json"
LOG_PATH = DATA_DIR / "app.log"

LEVELS = ["INFO", "WARNING", "ERROR"]


def generate_log_line(post: dict) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level = random.choice(LEVELS)
    message = post.get("title") or post.get("body", "")
    return f"[{timestamp}] {level} (user_id={post['userId']}, post_id={post['id']}): {message}"


def run_generate() -> None:
    try:
        with RAW_PATH.open("r", encoding="utf-8") as f:
            posts = json.load(f)
    except FileNotFoundError:
        print("Hata: raw_posts.json yok. Önce --fetch çalıştır.")
        return

    DATA_DIR.mkdir(exist_ok=True)
    with LOG_PATH.open("w", encoding="utf-8") as f:
        for post in posts:
            f.write(generate_log_line(post) + "\n")

    print("Log dosyası oluşturuldu → data/app.log")
