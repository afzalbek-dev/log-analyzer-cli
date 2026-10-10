import argparse
import sys
import json
import os
from .parser import LogParser
from .analyzer import LogMetricsAnalyzer


def main():
    parser = argparse.ArgumentParser(description="Log Analyzer CLI - Server loglarini tahlil qilish")
    parser.add_argument("logfile", help="access.log fayli yo'li")
    parser.add_argument("--top", type=int, default=5, help="Eng yuqori IP va URL lar soni")
    parser.add_argument("--json", action="store_true", help="JSON formatida chiqarish")

    args = parser.parse_args()

    if not os.path.exists(args.logfile):
        print(f"Log fayli topilmadi: {args.logfile}", file=sys.stderr)
        sys.exit(1)

    entries = []
    with open(args.logfile, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            entry = LogParser.parse_line(line)
            if entry:
                entries.append(entry)

    analyzer = LogMetricsAnalyzer(entries)
    summary = analyzer.get_summary(top_n=args.top)

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("=== NGINX / APACHE LOG TAHLILI ===")
        print(f"Jami so'rovlar : {summary['total_requests']}")
        print(f"Trafik hajmi   : {summary['total_bandwidth_mb']} MB\n")

        print("Status kodlari taqsimoti:")
        for status, pct in summary["status_percentages"].items():
            print(f"  • {status}: {pct}%")

        print(f"\nEng faol IP manzillar (Top {args.top}):")
        for item in summary["top_ips"]:
            print(f"  • {item['ip']}: {item['count']} ta so'rov")

        print(f"\nEng ko'p ochilgan sahifalar (Top {args.top}):")
        for item in summary["top_paths"]:
            print(f"  • {item['path']}: {item['count']} ta so'rov")


if __name__ == "__main__":
    main()
