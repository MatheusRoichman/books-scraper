from decimal import Decimal

from selectolax.parser import HTMLParser

from product import Product

def extract_products_from_page(html: HTMLParser, base_url: str):
  products_elements = html.css('.product_pod')

  rating_map = {
      "One": 1,
      "Two": 2,
      "Three": 3,
      "Four": 4,
      "Five": 5
  }

  products = []

  for product_element in products_elements:
    image = product_element.css_first("img.thumbnail")
    image_url = f"{base_url}{image.attributes.get('src')}"

    rating_element = product_element.css_first('.star-rating');
    rating_class = rating_element.attributes.get('class').split(' ')[1];
    rating = rating_map[rating_class]

    title_element = product_element.css_first('h3 > a')
    title = title_element.attributes.get('title')
    details_url = f"{base_url}{title_element.attributes.get('href')}"

    raw_price = product_element.css_first('.product_price > .price_color').text().strip()
    price = Decimal(raw_price.replace("£", ""))
    
    availability = product_element.css_first('.instock.availability').text().strip()

    product = Product(title=title, price=price, currency="GBP", availability=availability, rating=rating, image_url=image_url, details_url=details_url)
    products.append(product)

  return products