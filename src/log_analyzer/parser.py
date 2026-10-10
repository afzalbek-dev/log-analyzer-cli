import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class AccessLogEntry:
    ip: str
    timestamp_str: str
    method: str
    path: str
    status_code: int
    bytes_sent: int
    user_agent: str


class LogParser:
    """Nginx / Apache Combined Log Format satrlarini parsing qilish."""

    # Standart format: $remote_addr - $remote_user [$time_local] "$request" $status $body_bytes_sent "$http_referer" "$http_user_agent"
    COMBINED_LOG_REGEX = re.compile(
        r'^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"([A-Z]+)\s+([^"\s]+)(?:\s+HTTP\/[0-9\.]+)?\"\s+(\d{3})\s+(\d+|-)\s+"[^"]*"\s+"([^"]*)"'
    )

    @classmethod
    def parse_line(cls, line: str) -> Optional[AccessLogEntry]:
        line = line.strip()
        if not line:
            return None

        match = cls.COMBINED_LOG_REGEX.match(line)
        if match:
            ip = match.group(1)
            time_str = match.group(2)
            method = match.group(3)
            path = match.group(4)
            status = int(match.group(5))
            bytes_sent = int(match.group(6)) if match.group(6) != "-" else 0
            ua = match.group(7)
            return AccessLogEntry(ip, time_str, method, path, status, bytes_sent, ua)

        # Oddiy fallback parsing
        parts = line.split()
        if len(parts) >= 9:
            try:
                ip = parts[0]
                status = int(parts[8])
                return AccessLogEntry(
                    ip=ip,
                    timestamp_str="unknown",
                    method=parts[5].replace('"', '') if len(parts) > 5 else "GET",
                    path=parts[6] if len(parts) > 6 else "/",
                    status_code=status,
                    bytes_sent=int(parts[9]) if len(parts) > 9 and parts[9].isdigit() else 0,
                    user_agent="unknown",
                )
            except Exception:
                return None
        return None
