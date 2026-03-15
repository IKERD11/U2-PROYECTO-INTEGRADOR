import flet as ft
from components.product_card import build_product_card

# ── Flat Tokens ────────────────────────────────────────────────────
TEXT_SUB = "#94A3B8"

def build_favorites_panel(page, state, all_products, on_add_to_cart, on_toggle_fav, on_view_detail):
    grid_ref = ft.Ref[ft.Row]()

    def refresh_favs():
        fav_ids  = state.get_favorites()
        products = [p for p in all_products if p.id in fav_ids]

        if not products:
            grid_ref.current.controls = [
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.FAVORITE_BORDER_ROUNDED, size=80, color="#E2E8F0"),
                        ft.Text("Aún no tienes favoritos", size=18, color=TEXT_SUB, weight=ft.FontWeight.W_600),
                        ft.Text("Explora el catálogo y guarda lo que más te guste.", size=14, color=TEXT_SUB),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    alignment=ft.Alignment(0, 0), expand=True, padding=100
                )
            ]
        else:
            grid_ref.current.controls = [
                build_product_card(p, state, on_add_to_cart, on_toggle_fav, on_view_detail)
                for p in products
            ]

    grid = ft.ResponsiveRow(ref=grid_ref, spacing=20, run_spacing=20, alignment=ft.MainAxisAlignment.START)

    # Initial load
    fav_ids  = state.get_favorites()
    products = [p for p in all_products if p.id in fav_ids]
    if not products:
        grid.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.FAVORITE_BORDER_ROUNDED, size=80, color="#E2E8F0"),
                    ft.Text("Aún no tienes favoritos", size=18, color=TEXT_SUB, weight=ft.FontWeight.W_600),
                    ft.Text("Explora el catálogo y guarda lo que más te guste.", size=14, color=TEXT_SUB),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                alignment=ft.Alignment(0, 0), expand=True, padding=100
            )
        ]
    else:
        grid.controls = [
            build_product_card(p, state, on_add_to_cart, on_toggle_fav, on_view_detail)
            for p in products
        ]

    return ft.Container(
        expand=True, padding=ft.Padding.symmetric(horizontal=20, vertical=30),
        content=ft.Column([grid], scroll=ft.ScrollMode.HIDDEN, expand=True)
    ), refresh_favs
