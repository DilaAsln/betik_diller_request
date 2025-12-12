import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import List

from .models import LogRecord

REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"


def run_report(records: List[LogRecord]) -> None:
    REPORTS_DIR.mkdir(exist_ok=True)

    level_counts = Counter(r.level for r in records)
    user_stats = defaultdict(lambda: {"total": 0, "errors": 0})

    for r in records:
        user_stats[str(r.user_id)]["total"] += 1
        if r.is_error:
            user_stats[str(r.user_id)]["errors"] += 1

    error_messages = sorted(
        [r.message for r in records if r.is_error],
        key=len,
        reverse=True
    )[:5]

    summary = {
        "total_logs": len(records),
        "by_level": dict(level_counts),
        "by_user": dict(user_stats),
        "top_error_messages": error_messages,
    }

    with open(REPORTS_DIR / "summary.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["level", "count"])
        for level, count in level_counts.items():
            writer.writerow([level, count])

    with open(REPORTS_DIR / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Raporlar oluşturuldu → reports/")
