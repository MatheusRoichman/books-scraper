import json
import os
import time
from typing import Iterable

from scraper.product import Product


def save_products_to_json(
    products: Iterable[Product], folder: str = "responses"
) -> str:
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{time.time()}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump([p.to_dict() for p in products], f, indent=2, ensure_ascii=False)

    return path
