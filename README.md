# Python Scraper

An **async web scraper** built with **httpx** and **selectolax**, focused on clean architecture,
robust pagination handling, and maintainable parsing logic.

This project scrapes product data from paginated pages, parses HTML efficiently, and saves
structured results to JSON.

---

## ✨ Features

- ⚡ **Async HTTP requests** with controlled concurrency
- 🧠 **Fast HTML parsing** using Selectolax
- 📄 **Automatic pagination discovery**
- 💰 **Safe money handling** using `Decimal`
- 🧱 **Clean project structure** (parser, pagination, storage, HTTP client)
- 📦 **JSON output** with UTF-8 support
- 🧪 Sonar-friendly, low cognitive complexity parsing logic

---

## 📋 Requirements

- **Python 3.10+**
- macOS, Linux, or Windows

---

## 🚀 Setup

### 1️⃣ Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the scraper

```bash
python -m scraper.main
```

After execution:
- Products are scraped from all pages
- Results are saved to the `responses/` directory as JSON

---

## 📁 Project Structure

```
python-scraper/
├── pyproject.toml
├── requirements.txt
├── README.md
│
├── scraper/
│   ├── __init__.py
│   ├── main.py        # program entry point
│   ├── runner.py      # orchestration logic
│   ├── product.py     # Product data model
│   ├── parser.py      # HTML → Product parsing
│   ├── pagination.py  # pagination discovery
│   ├── http_client.py # async HTTP logic
│   └── storage.py     # JSON persistence
│
└── responses/          # scraped output
```

---

## 🧠 Design Decisions

- **Async-first**: Network I/O is the bottleneck, so async provides major speed gains.
- **Separation of concerns**:
  - HTTP fetching
  - HTML parsing
  - Pagination
  - Persistence
- **No recursion for pagination**: Safer and easier to reason about.
- **Decimal for prices**: Avoids floating-point precision issues.
- **Human-readable JSON**: UTF-8 output with indentation.

---

## 🔍 Example Output

```json
{
  "title": "A Light in the Attic",
  "price": "45.17",
  "currency": "GBP",
  "availability": "In stock",
  "rating": 3,
  "image_url": "...",
  "details_url": "..."
}
```

---

## ⚠️ Notes

- Concurrency is limited to avoid stressing the target website.
- Pagination is discovered dynamically from the first page.
- Parsing logic is defensive against missing or malformed HTML.

---

## 🛠️ Development

Recommended tools:

```bash
pip install black ruff mypy
```

Format and lint:
```bash
black .
ruff check .
```

---

## 🗺️ Possible Extensions

- CSV or SQLite export
- Retry & exponential backoff
- Progress logging (Page X / Y)
- Deduplication by product URL
- Unit tests for parser helpers
- CLI arguments (concurrency, output path)

---

## 📄 License

MIT
