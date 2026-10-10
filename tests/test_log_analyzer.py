import pytest
from log_analyzer.parser import LogParser
from log_analyzer.analyzer import LogMetricsAnalyzer


def test_log_line_parsing():
    sample_line = '192.168.1.100 - - [10/Oct/2026:14:32:10 +0500] "GET /api/v1/users HTTP/1.1" 200 1450 "-" "Mozilla/5.0"'
    entry = LogParser.parse_line(sample_line)

    assert entry is not None
    assert entry.ip == "192.168.1.100"
    assert entry.method == "GET"
    assert entry.path == "/api/v1/users"
    assert entry.status_code == 200
    assert entry.bytes_sent == 1450


def test_log_metrics_summary():
    lines = [
        '10.0.0.1 - - [date] "GET /index.html" 200 500 "-" "ua"',
        '10.0.0.1 - - [date] "GET /api/data" 200 1200 "-" "ua"',
        '10.0.0.2 - - [date] "GET /not-found" 404 150 "-" "ua"',
        '10.0.0.3 - - [date] "POST /login" 500 200 "-" "ua"',
    ]
    entries = [LogParser.parse_line(l) for l in lines if LogParser.parse_line(l)]
    assert len(entries) == 4

    analyzer = LogMetricsAnalyzer(entries)
    summary = analyzer.get_summary(top_n=2)

    assert summary["total_requests"] == 4
    assert summary["status_percentages"]["200"] == 50.0
    assert summary["status_percentages"]["404"] == 25.0
    assert summary["status_percentages"]["500"] == 25.0
    assert summary["top_ips"][0]["ip"] == "10.0.0.1"
    assert summary["top_ips"][0]["count"] == 2
