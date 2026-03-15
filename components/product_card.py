import flet as ft
from models.product import Product

# ── Design tokens ──────────────────────────────────────────────────
BG        = "#0B0F19"
SURFACE   = "#1A2235"
PRIMARY   = "#3B82F6"
SECONDARY = "#94A3B8"
SUCCESS   = "#10B981"
DANGER    = "#EF4444"
TEXT_MAIN = "#F8FAFC"
TEXT_SUB  = "#94A3B8"

CAT_COLORS = {
    "Wearables":  "#8B5CF6",
    "Audio":      "#F97316",
    "Periféricos":"#3B82F6",
    "Monitores":  "#06B6D4",
    "Portátiles": "#DB2777",
    "Gaming":     "#7C3AED",
    "Fotografía": "#EC4899",
    "Almacenamiento": "#6366F1",
    "PC":         "#2563EB",
    "Redes":      "#10B981",
    "Accesorios": "#F59E0B",
}

def build_stars(rating: float) -> ft.Row:
    stars = []
    for i in range(1, 6):
        if rating >= i:
            ico = ft.Icons.STAR_ROUNDED
        elif rating >= i - 0.5:
            ico = ft.Icons.STAR_HALF_ROUNDED
        else:
            ico = ft.Icons.STAR_OUTLINE_ROUNDED
        stars.append(ft.Icon(ico, color="#FBBF24", size=14))
    stars.append(ft.Text(f"{rating}", size=12, color=TEXT_SUB, weight=ft.FontWeight.W_600))
    return ft.Row(controls=stars, spacing=4)

def build_product_card(product: Product, state, on_add_to_cart, on_toggle_fav, on_view_detail):
    is_fav   = state.is_favorite(product.id)
    in_stock = product.stock > 0
    cat_color = CAT_COLORS.get(product.category, "#64748B")

    def add_cart(e):   on_add_to_cart(product)
    def toggle_fav(e):
        on_toggle_fav(product)
        is_now_fav = state.is_favorite(product.id)
        e.control.icon = ft.Icons.FAVORITE if is_now_fav else ft.Icons.FAVORITE_BORDER
        e.control.icon_color = DANGER if is_now_fav else TEXT_SUB
        e.control.update()

    def view_detail(e): on_view_detail(product)

    return ft.Container(
        col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
        bgcolor=SURFACE,
        border_radius=16,
        border=ft.Border.all(1, "#334155"),
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
        on_hover=lambda e: setattr(e.control, "shadow", ft.BoxShadow(blur_radius=30, color=ft.Colors.with_opacity(0.1, "#000"), offset=ft.Offset(0, 10)) if e.data == "true" else None) or e.control.update(),
        on_click=view_detail,
        content=ft.Column(
            spacing=0,
            controls=[
                # Image Section
                ft.Stack(
                    height=200,
                    controls=[
                        ft.Image(
                            src=product.image_path,
                            height=200,
                            width=float("inf"),
                            fit=ft.BoxFit.COVER,
                        ),
                        # Category Badge
                        ft.Container(
                            content=ft.Text(product.category.upper(), size=11, color=ft.Colors.WHITE, weight=ft.FontWeight.W_900),
                            bgcolor=cat_color,
                            padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                            border_radius=ft.BorderRadius.only(bottom_right=12, top_left=16),
                            left=0, top=0,
                        ),
                        # Favorite Button
                        ft.Container(
                            content=ft.IconButton(
                                icon=ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
                                icon_color=DANGER if is_fav else TEXT_SUB,
                                icon_size=18,
                                on_click=toggle_fav,
                                style=ft.ButtonStyle(
                                    shape=ft.CircleBorder(),
                                    bgcolor={ft.ControlState.HOVERED: "#1E293B", ft.ControlState.DEFAULT: "transparent"},
                                ),
                            ),
                            top=10, right=10,
                        ),
                        # Stock status
                        ft.Container(
                            content=ft.Row([
                                ft.Container(width=6, height=6, bgcolor=SUCCESS if in_stock else DANGER, border_radius=3),
                                ft.Text(
                                    "AGOTADO" if not in_stock else f"{product.stock} DISPONIBLES",
                                    size=9, color=TEXT_MAIN, weight=ft.FontWeight.W_700
                                ),
                            ], spacing=6),
                            bgcolor=ft.Colors.with_opacity(0.9, "#FFF"),
                            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
                            border_radius=20,
                            bottom=10, left=10,
                        ),
                    ]
                ),
                # Info Section
                ft.Container(
                    padding=20,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text(product.name, size=18, color=TEXT_MAIN, weight=ft.FontWeight.W_700, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
                            build_stars(product.rating),
                            ft.Text(product.description, size=13, color=TEXT_SUB, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text(f"${product.price:,.2f}", size=24, color=PRIMARY, weight=ft.FontWeight.W_800),
                                    ft.IconButton(
                                        icon=ft.Icons.ADD_SHOPPING_CART_ROUNDED,
                                        icon_size=20,
                                        icon_color=ft.Colors.WHITE,
                                        bgcolor=PRIMARY if in_stock else "#CBD5E1",
                                        disabled=not in_stock,
                                        on_click=add_cart,
                                        width=44, height=44,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                        )
                                    )
                                ]
                            )
                        ]
                    )
                )
            ]
        ),
        shadow=ft.BoxShadow(
            blur_radius=15,
            color=ft.Colors.with_opacity(0.04, "#000"),
            offset=ft.Offset(0, 4)
        )
    )
