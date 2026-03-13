from dataclasses import dataclass, field
from typing import List

@dataclass
class Product:
    """Modelo de datos para un artículo tecnológico."""
    id: int
    name: str
    description: str
    price: float
    image_path: str
    category: str = "General"
    stock: int = 10
    rating: float = 4.0
    images: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.images:
            self.images = [self.image_path]
