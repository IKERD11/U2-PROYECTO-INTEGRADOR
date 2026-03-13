import flet as ft
from models.product import Product

# ── Tokens ─────────────────────────────────────────────────────────
BG      = "#0F172A"
SURFACE = "#1E293B"
SURFACE2 = "#243347"
PRIMARY  = "#6366F1"
SUCCESS  = "#10B981"
DANGER   = "#EF4444"
TEXT_MAIN = "#F1F5F9"
TEXT_SUB  = "#94A3B8"

CAT_COLORS = {
    "Wearables":  "#7C3AED",
    "Audio":      "#EA580C",
    "Periféricos":"#2563EB",
    "Monitores":  "#0D9488",
    "General":    "#475569",
}


def build_stars(rating: float) -> ft.Row:
    stars = []
    for i in range(1, 6):
        if rating >= i:
            ico = ft.Icons.STAR
        elif rating >= i - 0.5:
            ico = ft.Icons.STAR_HALF
        else:
            ico = ft.Icons.STAR_BORDER
        stars.append(ft.Icon(ico, color="#FBBF24", size=14))
    stars.append(ft.Text(f"  {rating}", size=12, color=TEXT_SUB))
    return ft.Row(controls=stars, spacing=0)


def build_product_card(product: Product, state, on_add_to_cart, on_toggle_fav, on_view_detail):
    is_fav   = state.is_favorite(product.id)
    in_stock = product.stock > 0
    cat_color = CAT_COLORS.get(product.category, "#475569")

    def add_cart(e):   on_add_to_cart(product)
    def toggle_fav(e): on_toggle_fav(product)
    def view_detail(e): on_view_detail(product)

    # Image gradient overlay – name + category shown on top of photo
    image_section = ft.Stack(
        width=290, height=195,
        controls=[
            # Base image
            ft.Image(
                src=product.image_path, width=290, height=195,
                fit=ft.BoxFit.COVER,
                error_content=ft.Container(
                    content=ft.Column(
                        [ft.Icon(ft.Icons.BROKEN_IMAGE, size=40, color="#334155"),
                         ft.Text("Sin imagen", size=12, color="#475569")],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    alignment=ft.Alignment(0, 0),
                    bgcolor=BG, width=290, height=195,
                ),
            ),
            # Dark gradient overlay (bottom-heavy)
            ft.Container(
                gradient=ft.LinearGradient(
                    begin=ft.Alignment(0, 0),
                    end=ft.Alignment(0, 1),
                    colors=[
                        ft.Colors.with_opacity(0.0, BG),
                        ft.Colors.with_opacity(0.55, BG),
                        ft.Colors.with_opacity(0.97, BG),
                    ],
                ),
                width=290, height=195, top=0, left=0,
            ),
            # Stock badge (top-left)
            ft.Container(
                content=ft.Row([
                    ft.Icon(
                        ft.Icons.INVENTORY_2 if in_stock else ft.Icons.REMOVE_SHOPPING_CART,
                        size=10, color="#FFF",
                    ),
                    ft.Text(
                        f"  {product.stock} en stock" if in_stock else "  Agotado",
                        size=10, color="#FFF", weight=ft.FontWeight.BOLD,
                    ),
                ], spacing=0),
                bgcolor=ft.Colors.with_opacity(0.85, "#059669" if in_stock else DANGER),
                border_radius=ft.BorderRadius.all(20),
                padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                top=10, left=10,
            ),
            # Favorite button (top-right)
            ft.Container(
                content=ft.IconButton(
                    icon=ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
                    icon_color=DANGER, icon_size=18,
                    on_click=toggle_fav,
                    style=ft.ButtonStyle(padding=ft.Padding.all(4)),
                ),
                bgcolor=ft.Colors.with_opacity(0.75, "#000"),
                border_radius=ft.BorderRadius.all(20),
                top=8, right=8,
            ),
            # Category chip + product name at bottom
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text(product.category, size=10, color="#FFF", weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.with_opacity(0.9, cat_color),
                        border_radius=ft.BorderRadius.all(20),
                        padding=ft.Padding.symmetric(horizontal=9, vertical=3),
                    ),
                    ft.Text(product.name, size=15, color="#FFF", weight=ft.FontWeight.BOLD,
                            max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                ], spacing=4),
                bottom=10, left=12, right=12,
            ),
        ],
    )

    # Info section below image
    info_section = ft.Container(
        padding=ft.Padding.symmetric(horizontal=14, vertical=12),
        content=ft.Column(
            spacing=8,
            controls=[
                # Rating + description
                build_stars(product.rating),
                ft.Text(product.description, size=12, color=TEXT_SUB,
                        max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                ft.Divider(height=1, color=ft.Colors.with_opacity(0.08, "#FFF")),
                # Price + Cart
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column([
                            ft.Text("Precio", size=10, color=TEXT_SUB),
                            ft.Text(f"${product.price:,.2f}", size=20,
                                    color=SUCCESS, weight=ft.FontWeight.BOLD),
                        ], spacing=0),
                        ft.Button(
                            content=ft.Text("Carrito", size=12),
                            icon=ft.Icons.SHOPPING_CART_OUTLINED,
                            bgcolor=PRIMARY if in_stock else "#334155",
                            color="#FFF", disabled=not in_stock,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=12),
                                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                                elevation={"default": 4} if in_stock else {"default": 0},
                            ),
                            on_click=add_cart,
                        ),
                    ],
                ),
            ],
        ),
    )

    return ft.Container(
        width=290,
        bgcolor=SURFACE,
        border_radius=ft.BorderRadius.all(18),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.12, PRIMARY)),
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        shadow=ft.BoxShadow(
            spread_radius=0, blur_radius=30,
            color=ft.Colors.with_opacity(0.5, ft.Colors.BLACK),
            offset=ft.Offset(0, 12),
        ),
        ink=True,
        on_click=view_detail,
        content=ft.Column(controls=[image_section, info_section], spacing=0),
    )
