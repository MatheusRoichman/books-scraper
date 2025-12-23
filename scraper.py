from decimal import Decimal
from urllib.parse import urljoin
from selectolax.parser import HTMLParser

from product import Product

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def _safe_text(node, default: str = "") -> str:
    return node.text().strip() if node else default


def _normalize_spaces(text: str) -> str:
    return " ".join(text.split())


def _get_title_and_details(pod, base_url: str) -> tuple[str, str]:
    a = pod.css_first("h3 > a")
    if not a:
        return "", ""
    title = (a.attributes.get("title") or "").strip()
    details_url = urljoin(base_url, a.attributes.get("href") or "")
    return title, details_url


def _get_image_url(pod, base_url: str) -> str:
    img = pod.css_first("img.thumbnail")
    if not img:
        return ""
    return urljoin(base_url, img.attributes.get("src") or "")


def _get_rating(pod) -> int:
    rating_el = pod.css_first(".star-rating")
    if not rating_el:
        return 0

    classes = (rating_el.attributes.get("class") or "").split()
    rating_name = classes[1] if len(classes) > 1 else ""
    return RATING_MAP.get(rating_name, 0)


def _parse_price(raw_price: str) -> tuple[Decimal, str]:
    raw_price = raw_price.strip()
    if not raw_price:
        return Decimal("0"), ""

    currency = "GBP" if raw_price.startswith("£") else ""
    value = raw_price.replace("£", "")
    return Decimal(value), currency


def _get_price_and_currency(pod) -> tuple[Decimal, str]:
    price_el = pod.css_first(".product_price > .price_color")
    return _parse_price(_safe_text(price_el))


def _get_availability(pod) -> str:
    availability_el = pod.css_first(".instock.availability")
    return _normalize_spaces(_safe_text(availability_el))


def _pod_to_product(pod, base_url: str) -> Product | None:
    title, details_url = _get_title_and_details(pod, base_url)
    if not title or not details_url:
        return None

    image_url = _get_image_url(pod, base_url)
    rating = _get_rating(pod)
    price, currency = _get_price_and_currency(pod)
    availability = _get_availability(pod)

    return Product(
        title=title,
        price=price,
        currency=currency,
        availability=availability,
        rating=rating,
        image_url=image_url,
        details_url=details_url,
    )


def extract_products_from_page(doc: HTMLParser, base_url: str) -> list[Product]:
    products: list[Product] = []

    for pod in doc.css(".product_pod"):
        product = _pod_to_product(pod, base_url)
        if product:
            products.append(product)

    return products
