import flet as ft
from components.product_card import build_product_card

TEXT_MAIN = "#F1F5F9"
TEXT_SUB  = "#94A3B8"


def build_favorites_panel(page, state, all_products, on_add_to_cart, on_toggle_fav, on_view_detail):
    grid_ref  = ft.Ref[ft.Row]()
    empty_ref = ft.Ref[ft.Container]()

    def refresh_favorites():
        favs = [p for p in all_products if state.is_favorite(p.id)]
        if favs:
            empty_ref.current.visible = False
            grid_ref.current.controls = [
                build_product_card(p, state, on_add_to_cart, on_toggle_fav, on_view_detail)
                for p in favs
            ]
        else:
            empty_ref.current.visible = True
            grid_ref.current.controls = []

    empty_state = ft.Container(
        ref=empty_ref, visible=True, expand=True,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(height=60),
                ft.Icon(ft.Icons.FAVORITE_BORDER, size=90, color="#334155"),
                ft.Container(height=16),
                ft.Text("Aún no tienes favoritos", size=22, color=TEXT_MAIN, weight=ft.FontWeight.BOLD),
                ft.Text("Toca el corazón en un producto para añadirlo.", size=14, color=TEXT_SUB),
            ],
        ),
    )

    grid = ft.Row(
        ref=grid_ref, wrap=True, spacing=20, run_spacing=20,
        alignment=ft.MainAxisAlignment.CENTER, controls=[],
    )

    panel = ft.Container(
        expand=True, padding=ft.Padding.all(20),
        content=ft.Column(
            controls=[empty_state, grid],
            scroll=ft.ScrollMode.AUTO, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    return panel, refresh_favorites
