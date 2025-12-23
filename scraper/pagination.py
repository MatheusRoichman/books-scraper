import re
from urllib.parse import urljoin

from selectolax.parser import HTMLParser


def get_total_pages(doc: HTMLParser) -> int:
    el = doc.css_first(".pager .current")
    if not el:
        return 1
    text = " ".join(el.text().split())
    m = re.search(r"\d+$", text)
    return int(m.group()) if m else 1


def build_page_urls(base_url: str, total_pages: int) -> list[str]:
    urls = [base_url]
    for n in range(2, total_pages + 1):
        urls.append(urljoin(base_url, f"catalogue/page-{n}.html"))
    return urls
