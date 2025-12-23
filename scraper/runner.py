import asyncio
import time

import httpx
from selectolax.parser import HTMLParser

from scraper.config import BASE_URL, CONCURRENCY, HEADERS
from scraper.http_client import fetch
from scraper.pagination import build_page_urls, get_total_pages
from scraper.parser import extract_products_from_page
from scraper.storage import save_products_to_json

async def run():
    start = time.perf_counter()
    sem = asyncio.Semaphore(CONCURRENCY)

    async with httpx.AsyncClient(headers=HEADERS, timeout=20, follow_redirects=True) as client:
        page1_html = await fetch(client, BASE_URL, sem)
        page1_doc = HTMLParser(page1_html)

        total_pages = get_total_pages(page1_doc)
        urls = build_page_urls(BASE_URL, total_pages)

        rest_html = await asyncio.gather(*(fetch(client, u, sem) for u in urls[1:]))

    products = []
    products.extend(extract_products_from_page(page1_doc, BASE_URL))
    for html in rest_html:
        products.extend(extract_products_from_page(HTMLParser(html), BASE_URL))

    out_path = save_products_to_json(products)
    elapsed = time.perf_counter() - start

    print(f"Pages: {total_pages}")
    print(f"Products: {len(products)}")
    print(f"Saved: {out_path}")
    print(f"Total time: {elapsed:.2f}s")