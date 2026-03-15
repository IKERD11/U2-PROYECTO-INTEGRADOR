from models.product import Product


class AppState:
    """Estado global compartido: carrito y favoritos."""

    def __init__(self):
        self.cart: dict[int, dict] = {}   # {id: {"product": Product, "qty": int}}
        self.favorites: set[int] = set()  # ids de productos favoritos

    # ── Carrito ────────────────────────────────────────────────────
    def add_to_cart(self, product: Product):
        pid = product.id
        if pid in self.cart:
            self.cart[pid]["qty"] += 1
        else:
            self.cart[pid] = {"product": product, "qty": 1}

    def remove_from_cart(self, pid: int):
        self.cart.pop(pid, None)

    def update_cart_qty(self, pid: int, delta: int):
        if pid in self.cart:
            self.cart[pid]["qty"] += delta
            if self.cart[pid]["qty"] <= 0:
                del self.cart[pid]

    def clear_cart(self):
        self.cart.clear()

    def get_cart_count(self) -> int:
        return sum(item["qty"] for item in self.cart.values())

    def get_cart_total(self) -> float:
        return sum(item["product"].price * item["qty"] for item in self.cart.values())

    def get_cart_items(self) -> list:
        return list(self.cart.values())

    # ── Favoritos ──────────────────────────────────────────────────
    def toggle_favorite(self, pid: int):
        if pid in self.favorites:
            self.favorites.discard(pid)
        else:
            self.favorites.add(pid)

    def is_favorite(self, pid: int) -> bool:
        return pid in self.favorites

    def get_favorites(self) -> list[int]:
        return list(self.favorites)
