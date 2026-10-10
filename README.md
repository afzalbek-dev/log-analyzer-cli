# Log Analyzer CLI

Nginx va Apache veb-serverlarining `access.log` fayllarini yuqori tezlikda tahlil qiluvchi, HTTP status kodlari taqsimotini hisoblovchi, eng faol IP manzillar va 404 xatoliklarini aniqlovchi vosita.

## Xususiyatlari
- **Combined Log Format**: Nginx va Apache standart loglarini to'liq parsing qilish.
- **Status Taqsimoti**: 200 (muvaffaqiyat), 404 (topilmadi), 500 (server xatosi) foizli ulushini chiqarish.
- **Xavfsizlik va Botlar Tahlili**: Eng ko'p so'rov yuborgan IP manzillarni aniqlash (DDoS va bruteforce profilaktikasi).
- **JSON va Terminal Chiqishi**: CLI orqali qulay ko'rish yoki avtomatlashtirilgan cron skriptlar uchun JSON eksport.

## Foydalanish (Python)
```python
from log_analyzer import LogParser, LogMetricsAnalyzer

entries = [LogParser.parse_line(line) for line in open("/var/log/nginx/access.log")]
entries = [e for e in entries if e]

analyzer = LogMetricsAnalyzer(entries)
print(analyzer.get_summary(top_n=5))
```

## CLI
```bash
log-analyzer /var/log/nginx/access.log --top 10
log-analyzer /var/log/nginx/access.log --json
```

## Testlar
```bash
pytest tests/ -v
```

## Litsenziya
MIT
