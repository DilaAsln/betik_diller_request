import re
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from src.models import LogRecord


DATA_DIR = Path(__file__).resolve().parents[1] / "data"
LOG_PATH = DATA_DIR / "app.log"

LOG_REGEX = re.compile(
    r"\[(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    r"(?P<level>INFO|WARNING|ERROR) "
    r"\(user_id=(?P<user_id>\d+), post_id=(?P<post_id>\d+)\): "
    r"(?P<message>.*)"
)


def parse_log_line(line: str) -> Optional[LogRecord]:
    """
    >>> line = "[2025-12-09 14:23:15] ERROR (user_id=1, post_id=2): hata"
    >>> rec = parse_log_line(line)
    >>> rec.level
    'ERROR'
    >>> parse_log_line("bozuk") is None
    True
    """
    match = LOG_REGEX.match(line.strip())
    if not match:
        return None

    try:
        return LogRecord(
            timestamp=datetime.strptime(match["ts"], "%Y-%m-%d %H:%M:%S"),
            level=match["level"],
            user_id=int(match["user_id"]),
            post_id=int(match["post_id"]),
            message=match["message"],
        )
    except Exception:
        return None


def read_and_parse_log() -> List[LogRecord]:
    records = []
    try:
        with LOG_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                rec = parse_log_line(line)
                if rec:
                    records.append(rec)
    except FileNotFoundError:
        print("Hata: app.log bulunamadı.")
    return records
