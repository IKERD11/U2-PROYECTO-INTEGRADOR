import flet as ft
from state.app_state import AppState
from data.repository import get_products
from models.product import Product
from components.product_card import build_stars
from views.catalog_view import build_catalog_panel
from views.favorites_view import build_favorites_panel

# ── Dark Theme Tokens ─────────────────────────────────────────────
BG        = "#0B0F19"
SURFACE   = "#1A2235"
PRIMARY   = "#3B82F6"
SECONDARY = "#94A3B8"
TEXT_MAIN = "#F8FAFC"
TEXT_SUB  = "#94A3B8"
ACCENT    = "#60A5FA"

def main(page: ft.Page):
    page.title = "TechStore — Premium Experience"
    page.bgcolor = BG
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    import os
    page.window_width = 390 if os.getenv("FLET_MOBILE") else 1200
    page.window_height = 844 if os.getenv("FLET_MOBILE") else 900
    
    # We remove custom Inter font to prevent CORS issues on Web, 
    # letting it gracefully fallback to system fonts or built-ins.
    page.theme = ft.Theme()

    def get_is_mobile():
        # Ensure page.width is available
        width = page.width if page.width else 1200
        return width < 800

    main_container_ref = ft.Ref[ft.Column]()

    state = AppState()
    all_products = get_products()

    badge_ref      = ft.Ref[ft.Container]()
    badge_text_ref = ft.Ref[ft.Text]()

    main_dialog = ft.AlertDialog(modal=True, bgcolor=SURFACE, shape=ft.RoundedRectangleBorder(radius=20), content=ft.Container())
    page.overlay.append(main_dialog)

    def close_dialog(e=None):
        main_dialog.open = False
        refresh_catalog()
        refresh_favs()
        page.update()

    def update_badge():
        count = state.get_cart_count()
        badge_ref.current.visible = count > 0
        badge_text_ref.current.value = str(count)
        page.update()

    # ── CART DIALOG ────────────────────────────────────────────────
    cart_body = ft.Column(controls=[], scroll=ft.ScrollMode.HIDDEN, height=400, spacing=15)

    def _refresh_cart():
        items = state.get_cart_items()
        if not items:
            cart_body.controls = [ft.Container(
                content=ft.Column(
                    [ft.Icon(ft.Icons.SHOPPING_BAG_OUTLINED, size=64, color="#E2E8F0"),
                     ft.Text("Tu carrito está vacío", size=16, color=TEXT_SUB, weight=ft.FontWeight.W_500)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                alignment=ft.Alignment(0, 0), height=300,
            )]
        else:
            rows = []
            for item in items:
                p, qty = item["product"], item["qty"]
                pid = p.id
                def dec(pid=pid): state.update_cart_qty(pid, -1); update_badge(); _refresh_cart(); page.update()
                def inc(pid=pid): state.update_cart_qty(pid, 1); update_badge(); _refresh_cart(); page.update()
                def rem(pid=pid): state.remove_from_cart(pid); update_badge(); _refresh_cart(); page.update()

                rows.append(ft.Container(
                    content=ft.Row([
                        ft.Image(src=p.image_path, width=70, height=70, fit=ft.BoxFit.COVER, border_radius=12),
                        ft.Column([
                            ft.Text(p.name, size=15, weight=ft.FontWeight.W_700, color=TEXT_MAIN, max_lines=1),
                            ft.Text(f"${p.price:,.2f}", size=14, color=PRIMARY, weight=ft.FontWeight.W_600),
                        ], expand=True, spacing=4),
                        ft.Row([
                            ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE_ROUNDED, icon_color=TEXT_SUB, icon_size=20, on_click=lambda e, f=dec: f()),
                            ft.Text(str(qty), size=14, weight=ft.FontWeight.W_700, width=30, text_align=ft.TextAlign.CENTER),
                            ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE_ROUNDED, icon_color=PRIMARY, icon_size=20, on_click=lambda e, f=inc: f()),
                        ], spacing=0),
                        ft.IconButton(ft.Icons.DELETE_OUTLINE_ROUNDED, icon_color="#EF4444", icon_size=22, on_click=lambda e, f=rem: f()),
                    ], spacing=15),
                    padding=ft.Padding.symmetric(vertical=10),
                    border=ft.Border(bottom=ft.BorderSide(1, "#F1F5F9")),
                ))
            
            rows.append(ft.Container(
                content=ft.Row([
                    ft.Text("Total", weight=ft.FontWeight.W_500, size=16, color=TEXT_SUB),
                    ft.Text(f"${state.get_cart_total():,.2f}", size=26, color=TEXT_MAIN, weight=ft.FontWeight.W_900),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding.only(top=20),
            ))
            cart_body.controls = rows

    def open_cart(e=None):
        _refresh_cart()
        main_dialog.title = ft.Row(
            [
                ft.Text("Mi Carrito", weight=ft.FontWeight.W_800, size=24),
                ft.IconButton(ft.Icons.CLOSE_ROUNDED, icon_color=TEXT_MAIN, on_click=close_dialog)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        main_dialog.content = cart_body
        main_dialog.actions = [
            ft.TextButton("VACIAR", icon=ft.Icons.DELETE_SWEEP_ROUNDED, style=ft.ButtonStyle(color="#EF4444"), on_click=lambda e: [state.clear_cart(), update_badge(), _refresh_cart(), page.update()]),
            ft.ElevatedButton("PAGAR AHORA", bgcolor=PRIMARY, color="#FFFFFF", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=close_dialog),
        ]
        main_dialog.open = True
        page.update()

    # ── DETAIL DIALOG ──────────────────────────────────────────────
    def open_detail(product: Product):
        def add(e):
            state.add_to_cart(product)
            update_badge()
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"¡{product.name} añadido al carrito!", color="#FFFFFF"), 
                bgcolor="#10B981", 
                duration=2000
            )
            page.snack_bar.open = True
            page.update()

        def fav(e):
            state.toggle_favorite(product.id)
            is_fav = state.is_favorite(product.id)
            e.control.icon = ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_OUTLINE_ROUNDED
            e.control.update()

        is_mobile = get_is_mobile()
        dialog_width = None if is_mobile else 700
        img_height   = 220 if is_mobile else 350
        title_size   = 20 if is_mobile else 28
        price_size   = 22 if is_mobile else 32

        main_dialog.title = None
        main_dialog.content = ft.Container(
            width=dialog_width,
            content=ft.Column(scroll=ft.ScrollMode.HIDDEN, controls=[
                ft.Stack([
                    ft.Image(src=product.image_path, height=img_height, fit=ft.BoxFit.COVER, border_radius=16,
                             width=float("inf")),
                    ft.Container(
                        content=ft.IconButton(ft.Icons.CLOSE_ROUNDED, icon_color=TEXT_MAIN, bgcolor=SURFACE, on_click=close_dialog),
                        top=10, right=10
                    )
                ]),
                ft.Container(padding=ft.Padding.symmetric(horizontal=16 if is_mobile else 20, vertical=10),
                             content=ft.Column([
                    ft.Row([
                        ft.Column([
                            ft.Text(product.category.upper(), size=11, color=PRIMARY, weight=ft.FontWeight.W_800),
                            ft.Text(product.name, size=title_size, weight=ft.FontWeight.W_800, color=TEXT_MAIN, max_lines=2),
                        ], spacing=4, expand=True),
                        ft.Text(f"${product.price:,.2f}", size=price_size, color=TEXT_MAIN, weight=ft.FontWeight.W_900),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=is_mobile),
                    ft.Row([build_stars(product.rating), ft.Text(f"({product.stock} disponibles)", color=TEXT_SUB, size=13)]),
                    ft.Divider(height=20, color="#F1F5F9"),
                    ft.Text(product.description, size=14 if is_mobile else 16, color=TEXT_SUB),
                    ft.Container(height=10),
                    ft.Row([
                        ft.ElevatedButton(
                            content=ft.Row([ft.Icon(ft.Icons.ADD_SHOPPING_CART_ROUNDED), ft.Text("AÑADIR AL CARRITO", weight=ft.FontWeight.W_700)], alignment=ft.MainAxisAlignment.CENTER),
                            bgcolor=PRIMARY, color="#FFF", expand=True, height=50,
                            disabled=product.stock <= 0, on_click=add,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                        ),
                        ft.IconButton(
                            icon=ft.Icons.FAVORITE if state.is_favorite(product.id) else ft.Icons.FAVORITE_OUTLINE_ROUNDED,
                            icon_color="#EF4444", on_click=fav, width=50, height=50,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), side=ft.BorderSide(1, "#F1F5F9"))
                        )
                    ], spacing=12)
                ], spacing=10))
            ])
        )
        main_dialog.actions = []
        main_dialog.open = True
        page.update()

    # ── CALLBACKS ──────────────────────────────────────────────────
    def on_add(p):
        state.add_to_cart(p)
        update_badge()
        page.snack_bar = ft.SnackBar(
            content=ft.Text(f"¡{p.name} añadido al carrito!", color="#FFFFFF"), 
            bgcolor="#10B981", 
            duration=2000
        )
        page.snack_bar.open = True
        page.update()
        
    def on_fav(p): state.toggle_favorite(p.id)

    catalog_panel, refresh_catalog = build_catalog_panel(page, state, all_products, on_add, on_fav, open_detail)
    favorites_panel, refresh_favs = build_favorites_panel(page, state, all_products, on_add, on_fav, open_detail)

    # ── NAVIGATION ──
    content_area_ref = ft.Ref[ft.Container]()
    panels = [catalog_panel, favorites_panel]
    tab_indicator_refs = [ft.Ref[ft.Container](), ft.Ref[ft.Container]()]
    tab_labels = ["Explorar Catálogo", "Mis Favoritos"]

    def switch_tab(idx: int):
        if idx == 0:
            refresh_catalog()
        elif idx == 1:
            refresh_favs()
        content_area_ref.current.content = panels[idx]
        for i, ref in enumerate(tab_indicator_refs):
            ref.current.bgcolor = PRIMARY if i == idx else "transparent"
            ref.current.width = 40 if i == idx else 0
        page.update()

    nav_bar = ft.Container(
        bgcolor=SURFACE, border=ft.Border(bottom=ft.BorderSide(1, "#1E293B")),
        padding=ft.Padding.symmetric(horizontal=60),
        height=70,
        content=ft.Row([
            ft.Row([
                ft.Container(
                    on_click=lambda e, i=idx: switch_tab(i),
                    content=ft.Column([
                        ft.Text(label, size=14, weight=ft.FontWeight.W_600, color=TEXT_MAIN),
                        ft.Container(ref=tab_indicator_refs[idx], height=3, width=40 if idx==0 else 0, bgcolor=PRIMARY, border_radius=2, animate=300)
                    ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding.only(top=24),
                ) for idx, label in enumerate(tab_labels)
            ], spacing=40),
            ft.Row([
                ft.Stack([
                    ft.IconButton(ft.Icons.SHOPPING_BAG_OUTLINED, icon_size=24, icon_color=TEXT_MAIN, on_click=open_cart),
                    ft.Container(
                        ref=badge_ref, visible=False,
                        content=ft.Text("0", ref=badge_text_ref, size=12, color=ft.colors.WHITE, weight=ft.FontWeight.W_900, text_align=ft.TextAlign.CENTER),
                        bgcolor=ft.colors.RED_500, width=20, height=20, border_radius=10, 
                        alignment=ft.alignment.center, right=2, top=2
                    )
                ]),
                ft.CircleAvatar(foreground_image_src="https://api.dicebear.com/7.x/avataaars/svg?seed=Lucky", radius=16)
            ], spacing=20)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # ── PREMIUM HEADER ──────────────────────────────────────────────
    header_title_ref = ft.Ref[ft.Text]()
    header_sub_ref   = ft.Ref[ft.Text]()
    header = ft.Container(
        bgcolor=SURFACE, padding=ft.Padding.symmetric(horizontal=60, vertical=40),
        content=ft.Row([
            ft.Column([
                ft.Row([
                    ft.Container(width=12, height=12, bgcolor=PRIMARY, border_radius=3),
                    ft.Text("TECHSTORE", size=14, weight=ft.FontWeight.W_800, color=PRIMARY),
                ], spacing=10),
                ft.Text(ref=header_title_ref, value="Innovación Digital", size=48, weight=ft.FontWeight.W_900, color=TEXT_MAIN),
                ft.Text(ref=header_sub_ref, value="Descubre la selección más exclusiva de gadgets y periféricos.", size=16, color=TEXT_SUB, max_lines=2),
            ], spacing=10, expand=True, tight=True),
            ft.Container(
                content=ft.Icon(ft.Icons.BOLT_ROUNDED, size=80, color=ft.Colors.with_opacity(0.05, PRIMARY)),
                alignment=ft.Alignment(1, 0)
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    # ── RESPONSIVE BUILDER ──────────────────────────────────────────
    def build_app():
        is_mobile = get_is_mobile()
        px = 12 if is_mobile else 60

        # Update Header
        header.padding = ft.Padding.symmetric(horizontal=px, vertical=20 if is_mobile else 40)
        header_row = header.content
        header_row.wrap = is_mobile
        header_row.controls[0].expand = not is_mobile
        if header_title_ref.current:
            header_title_ref.current.size = 28 if is_mobile else 48
        if header_sub_ref.current:
            header_sub_ref.current.size = 13 if is_mobile else 16
            header_sub_ref.current.visible = not is_mobile  # hide subtitle on very small screens

        # Update Nav Bar
        nav_bar.padding = ft.Padding.symmetric(horizontal=px)
        nav_bar.content.wrap = is_mobile
        for child in nav_bar.content.controls:
            if hasattr(child, "wrap"):
                child.wrap = is_mobile
        nav_bar.height = None if is_mobile else 70

        # Update Content Area
        if content_area_ref.current:
            content_area_ref.current.padding = ft.Padding.only(left=px, right=px, bottom=px)

        page.update()

    page.on_resize = lambda e: build_app()

    page.add(ft.Column(ref=main_container_ref, controls=[nav_bar, ft.Container(ref=content_area_ref, content=catalog_panel, expand=True)], expand=True, spacing=0))
    build_app()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
