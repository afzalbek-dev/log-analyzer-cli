from collections import Counter
from typing import List, Dict, Any
from .parser import AccessLogEntry


class LogMetricsAnalyzer:
    """Log yozuvlaridan statistika, anomaliyalar va xatoliklar ulushini hisoblash."""

    def __init__(self, entries: List[AccessLogEntry]):
        self.entries = entries

    def get_summary(self, top_n: int = 5) -> Dict[str, Any]:
        if not self.entries:
            return {"total_requests": 0, "status_breakdown": {}, "top_ips": [], "top_paths": []}

        total_requests = len(self.entries)
        total_bytes = sum(e.bytes_sent for e in self.entries)

        status_counts = Counter(e.status_code for e in self.entries)
        ip_counts = Counter(e.ip for e in self.entries)
        path_counts = Counter(e.path for e in self.entries)
        error_404_counts = Counter(e.path for e in self.entries if e.status_code == 404)

        status_percentages = {
            f"{status}": round((count / total_requests) * 100, 2)
            for status, count in status_counts.items()
        }

        return {
            "total_requests": total_requests,
            "total_bandwidth_mb": round(total_bytes / (1024 * 1024), 2),
            "status_percentages": status_percentages,
            "top_ips": [{"ip": ip, "count": c} for ip, c in ip_counts.most_common(top_n)],
            "top_paths": [{"path": p, "count": c} for p, c in path_counts.most_common(top_n)],
            "top_404_paths": [{"path": p, "count": c} for p, c in error_404_counts.most_common(top_n)],
        }
