from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Product:
    title: str
    price: Decimal
    currency: str
    availability: str
    rating: int
    image_url: str
    details_url: str

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "price": str(self.price),
            "currency": self.currency,
            "availability": self.availability,
            "rating": self.rating,
            "image_url": self.image_url,
            "details_url": self.details_url,
        }