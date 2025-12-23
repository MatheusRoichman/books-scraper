import asyncio
import json
import os
import re
import time
from dataclasses import dataclass
from decimal import Decimal
from typing import List
from urllib.parse import urljoin

import httpx
from selectolax.parser import HTMLParser

from product import Product
from scraper import extract_products_from_page


BASE_URL = "https://books.toscrape.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}
CONCURRENCY = 10


def get_total_pages(doc: HTMLParser) -> int:
    el = doc.css_first(".pager .current")
    if not el:
        return 1
    text = " ".join(el.text().split())
    m = re.search(r"\d+$", text)
    return int(m.group()) if m else 1


def build_page_urls(base_url: str, total_pages: int) -> List[str]:
    urls = [base_url]
    for n in range(2, total_pages + 1):
        urls.append(urljoin(base_url, f"catalogue/page-{n}.html"))
    return urls


async def fetch(client: httpx.AsyncClient, url: str, sem: asyncio.Semaphore) -> str:
    async with sem:
        r = await client.get(url)
        r.raise_for_status()
        return r.text


async def scrape_all_products(base_url: str) -> List[Product]:
    sem = asyncio.Semaphore(CONCURRENCY)

    async with httpx.AsyncClient(headers=HEADERS, timeout=20, follow_redirects=True) as client:
        page1_html = await fetch(client, base_url, sem)
        page1_doc = HTMLParser(page1_html)

        total_pages = get_total_pages(page1_doc)
        page_urls = build_page_urls(base_url, total_pages)

        remaining_html_pages = await asyncio.gather(
            *(fetch(client, url, sem) for url in page_urls[1:])
        )

    products: List[Product] = []
    products.extend(extract_products_from_page(page1_doc, base_url))

    for html_text in remaining_html_pages:
        doc = HTMLParser(html_text)
        products.extend(extract_products_from_page(doc, base_url))

    return products


def save_products_to_json(products: List[Product], folder: str = "responses") -> str:
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{time.time()}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in products], f, indent=2, ensure_ascii=False)

    return path


async def main():
    start = time.perf_counter()

    products = await scrape_all_products(BASE_URL)

    elapsed = time.perf_counter() - start

    out_path = save_products_to_json(products)

    print(f"Scraped {len(products)} products")
    print(f"Saved to: {out_path}")
    print(f"Total time: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
