import flet as ft
from state.app_state import AppState
from data.repository import get_products
from models.product import Product
from components.product_card import build_stars
from views.catalog_view import build_catalog_panel
from views.favorites_view import build_favorites_panel

# ── Design tokens ──────────────────────────────────────────────────
BG      = "#0F172A"
SURFACE = "#1E293B"
PRIMARY = "#6366F1"
SECONDARY = "#22D3EE"
SUCCESS = "#10B981"
DANGER  = "#EF4444"
TEXT_MAIN = "#F1F5F9"
TEXT_SUB  = "#94A3B8"


def main(page: ft.Page):
    page.title = "TechStore"
    page.bgcolor = BG
    page.padding = ft.Padding.all(0)
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_min_width = 800

    state = AppState()
    all_products = get_products()

    # Refs para el badge del carrito
    badge_ref      = ft.Ref[ft.Container]()
    badge_text_ref = ft.Ref[ft.Text]()

    # Único diálogo reutilizable
    main_dialog = ft.AlertDialog(modal=True, bgcolor=SURFACE)
    page.dialog = main_dialog

    def close_dialog(e=None):
        main_dialog.open = False
        page.update()

    def update_badge():
        count = state.get_cart_count()
        badge_ref.current.visible = count > 0
        badge_text_ref.current.value = str(count)

    # ── CARRITO ────────────────────────────────────────────────────
    cart_body = ft.Column(controls=[], scroll=ft.ScrollMode.AUTO, width=430, height=370)

    def build_cart_rows():
        items = state.get_cart_items()
        if not items:
            return [ft.Container(
                content=ft.Column(
                    [ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=64, color="#334155"),
                     ft.Text("El carrito está vacío", size=16, color=TEXT_SUB)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment(0, 0), height=200,
            )]

        rows = []
        for item in items:
            p: Product = item["product"]
            qty: int   = item["qty"]
            pid = p.id

            def mk_dec(pid=pid):
                def fn(e): state.update_cart_qty(pid, -1); update_badge(); _refresh_cart(); page.update()
                return fn

            def mk_inc(pid=pid):
                def fn(e): state.update_cart_qty(pid, 1); update_badge(); _refresh_cart(); page.update()
                return fn

            def mk_del(pid=pid):
                def fn(e): state.remove_from_cart(pid); update_badge(); _refresh_cart(); page.update()
                return fn

            rows.append(ft.Container(
                content=ft.Row(controls=[
                    ft.Image(src=p.image_path, width=50, height=50, fit=ft.BoxFit.COVER,
                             error_content=ft.Icon(ft.Icons.IMAGE, size=30, color="#475569")),
                    ft.Column([
                        ft.Text(p.name, size=13, weight=ft.FontWeight.BOLD, color=TEXT_MAIN,
                                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, width=160),
                        ft.Text(f"${p.price:,.2f}", size=12, color=SUCCESS),
                    ], spacing=2, expand=True),
                    ft.Row([
                        ft.IconButton(ft.Icons.REMOVE_CIRCLE, icon_color=DANGER, icon_size=20, on_click=mk_dec()),
                        ft.Text(str(qty), size=14, weight=ft.FontWeight.BOLD, width=28,
                                text_align=ft.TextAlign.CENTER, color=TEXT_MAIN),
                        ft.IconButton(ft.Icons.ADD_CIRCLE, icon_color=SUCCESS, icon_size=20, on_click=mk_inc()),
                    ], spacing=0),
                    ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="#475569", icon_size=20, on_click=mk_del()),
                ]),
                padding=ft.Padding.symmetric(vertical=8),
                border=ft.Border(bottom=ft.BorderSide(1, "#334155")),
            ))

        total = state.get_cart_total()
        rows += [
            ft.Container(height=8),
            ft.Container(
                content=ft.Row([
                    ft.Text("TOTAL", weight=ft.FontWeight.BOLD, size=15, color=TEXT_SUB),
                    ft.Text(f"${total:,.2f}", weight=ft.FontWeight.BOLD, size=24, color=SUCCESS),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding.symmetric(vertical=8),
            ),
        ]
        return rows

    def _refresh_cart():
        cart_body.controls = build_cart_rows()

    def open_cart(e=None):
        _refresh_cart()
        main_dialog.title = ft.Row([
            ft.Icon(ft.Icons.SHOPPING_CART, color=PRIMARY, size=24),
            ft.Text("  Carrito de Compras", weight=ft.FontWeight.BOLD, size=20, color=TEXT_MAIN),
        ])
        main_dialog.content = cart_body
        main_dialog.actions = [
            ft.TextButton("Vaciar todo", style=ft.ButtonStyle(color=DANGER),
                          on_click=lambda e: [state.clear_cart(), update_badge(), _refresh_cart(), page.update()]),
            ft.Button(content=ft.Text("Cerrar"), bgcolor=PRIMARY, color="#FFF", on_click=close_dialog),
        ]
        main_dialog.actions_alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        main_dialog.open = True
        page.update()

    # ── DETALLE ────────────────────────────────────────────────────
    def open_detail(product: Product):
        in_stock = product.stock > 0

        def add_from_detail(e):
            state.add_to_cart(product); update_badge(); page.update()

        def fav_from_detail(e):
            state.toggle_favorite(product.id)
            refresh_catalog(); refresh_favs()
            open_detail(product)  # reabrir con estado actualizado

        main_dialog.title = ft.Text(product.name, weight=ft.FontWeight.BOLD, size=20, color=TEXT_MAIN)
        main_dialog.content = ft.Column(scroll=ft.ScrollMode.AUTO, width=500, controls=[
            ft.Container(
                content=ft.Image(src=product.image_path, width=500, height=220, fit=ft.BoxFit.COVER,
                                 error_content=ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=50, color="#475569")),
                border_radius=ft.BorderRadius.all(12), clip_behavior=ft.ClipBehavior.HARD_EDGE,
            ),
            ft.Container(height=12),
            ft.Row([
                ft.Text(f"${product.price:,.2f}", size=28, color=SUCCESS, weight=ft.FontWeight.BOLD),
                build_stars(product.rating),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=6),
            ft.Text(
                f"✓ En stock: {product.stock} uds." if in_stock else "✗ Agotado",
                size=13, color=SUCCESS if in_stock else DANGER, weight=ft.FontWeight.W_600,
            ),
            ft.Container(height=8),
            ft.Text(product.description, size=14, color=TEXT_SUB),
            ft.Container(height=16),
            ft.Row([
                ft.Button(
                    content=ft.Text("Agregar al carrito"), icon=ft.Icons.SHOPPING_CART,
                    bgcolor=PRIMARY if in_stock else "#334155", color="#FFF",
                    disabled=not in_stock, on_click=add_from_detail,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                ),
                ft.Button(
                    content=ft.Text("Quitar favorito" if state.is_favorite(product.id) else "Favorito"),
                    icon=ft.Icons.FAVORITE if state.is_favorite(product.id) else ft.Icons.FAVORITE_BORDER,
                    bgcolor="#7F1D1D" if state.is_favorite(product.id) else "#1E3A5F",
                    color="#FFF", on_click=fav_from_detail,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                ),
            ], spacing=12),
        ])
        main_dialog.actions = [
            ft.Button(content=ft.Text("Cerrar"), bgcolor=SURFACE, color=TEXT_MAIN, on_click=close_dialog)
        ]
        main_dialog.actions_alignment = ft.MainAxisAlignment.END
        main_dialog.open = True
        page.update()

    # ── CALLBACKS compartidos ──────────────────────────────────────
    def on_add_to_cart(product: Product):
        state.add_to_cart(product); update_badge(); page.update()

    def on_toggle_fav(product: Product):
        state.toggle_favorite(product.id)
        refresh_catalog(); refresh_favs(); page.update()

    # ── Construir vistas ───────────────────────────────────────────
    catalog_panel, refresh_catalog = build_catalog_panel(
        page, state, all_products, on_add_to_cart, on_toggle_fav, open_detail,
    )
    favorites_panel, refresh_favs = build_favorites_panel(
        page, state, all_products, on_add_to_cart, on_toggle_fav, open_detail,
    )

    # ── CONTENIDO ACTIVO ──────────────────────────────────────────
    content_area_ref = ft.Ref[ft.Container]()
    panels = [catalog_panel, favorites_panel]
    active_tab = {"idx": 0}

    tab_indicator_refs = [ft.Ref[ft.Container](), ft.Ref[ft.Container]()]
    tab_label_refs     = [ft.Ref[ft.Text](),      ft.Ref[ft.Text]()]
    tab_icon_refs      = [ft.Ref[ft.Icon](),       ft.Ref[ft.Icon]()]
    tab_container_refs = [ft.Ref[ft.Container](), ft.Ref[ft.Container]()]

    TAB_ICONS  = [ft.Icons.STORE_OUTLINED, ft.Icons.FAVORITE_BORDER]
    TAB_ACTIVE = [ft.Icons.STORE, ft.Icons.FAVORITE]

    def switch_tab(idx: int):
        active_tab["idx"] = idx
        content_area_ref.current.content = panels[idx]
        for i in range(2):
            is_a = i == idx
            tab_container_refs[i].current.bgcolor = ft.Colors.with_opacity(0.15, PRIMARY) if is_a else "transparent"
            tab_indicator_refs[i].current.visible = is_a
            tab_label_refs[i].current.color   = "#FFFFFF" if is_a else TEXT_SUB
            tab_label_refs[i].current.weight  = ft.FontWeight.BOLD if is_a else ft.FontWeight.NORMAL
            tab_icon_refs[i].current.name     = TAB_ACTIVE[i] if is_a else TAB_ICONS[i]
            tab_icon_refs[i].current.color    = PRIMARY if is_a else TEXT_SUB
        page.update()

    def make_tab_btn(label, icon_name, active_icon, idx):
        is_a = idx == 0
        def on_click(e): switch_tab(idx)
        return ft.Container(
            ref=tab_container_refs[idx],
            on_click=on_click, ink=True,
            border_radius=ft.BorderRadius.all(10),
            margin=ft.Margin.all(6),
            padding=ft.Padding.symmetric(horizontal=24, vertical=10),
            bgcolor=ft.Colors.with_opacity(0.15, PRIMARY) if is_a else "transparent",
            content=ft.Row([
                ft.Icon(active_icon if is_a else icon_name, ref=tab_icon_refs[idx],
                        size=18, color=PRIMARY if is_a else TEXT_SUB),
                ft.Text(label, ref=tab_label_refs[idx], size=14,
                        color="#FFF" if is_a else TEXT_SUB,
                        weight=ft.FontWeight.BOLD if is_a else ft.FontWeight.NORMAL),
                ft.Container(
                    ref=tab_indicator_refs[idx], visible=is_a,
                    width=6, height=6, border_radius=ft.BorderRadius.all(3),
                    bgcolor=PRIMARY,
                ),
            ], spacing=8),
        )

    tab_bar = ft.Container(
        bgcolor=SURFACE,
        border=ft.Border(bottom=ft.BorderSide(1, ft.Colors.with_opacity(0.07, "#FFF"))),
        padding=ft.Padding.symmetric(horizontal=16, vertical=0),
        content=ft.Row(controls=[
            make_tab_btn("Catálogo",  ft.Icons.STORE_OUTLINED, ft.Icons.STORE,     0),
            make_tab_btn("Favoritos", ft.Icons.FAVORITE_BORDER, ft.Icons.FAVORITE, 1),
        ], spacing=4),
    )

    # ── HEADER ─────────────────────────────────────────────────────
    # Diagonal gradient for a more dynamic look
    header = ft.Container(
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=["#4F46E5", PRIMARY, "#0EA5E9"],
        ),
        padding=ft.Padding.symmetric(horizontal=32, vertical=18),
        shadow=ft.BoxShadow(
            spread_radius=0, blur_radius=40,
            color=ft.Colors.with_opacity(0.5, PRIMARY),
            offset=ft.Offset(0, 8),
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                # Logo + tagline
                ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.STOREFRONT_ROUNDED, size=32, color="#FFF"),
                        ft.Text("  TechStore", size=26, weight=ft.FontWeight.W_900, color="#FFF"),
                    ], spacing=0),
                    ft.Text("Tecnología de vanguardia", size=12,
                            color=ft.Colors.with_opacity(0.7, "#FFF")),
                ], spacing=2),
                # Cart button – glowing badge
                ft.Stack(width=54, height=54, controls=[
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.SHOPPING_CART_OUTLINED,
                            icon_color="#FFF", icon_size=26,
                            tooltip="Ver carrito", on_click=open_cart,
                        ),
                        bgcolor=ft.Colors.with_opacity(0.2, "#FFF"),
                        border_radius=ft.BorderRadius.all(14),
                        width=48, height=48, top=3, left=3,
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.3, "#FFF")),
                    ),
                    ft.Container(
                        ref=badge_ref, visible=False,
                        content=ft.Text("0", ref=badge_text_ref, size=9, color="#FFF",
                                        weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        bgcolor=DANGER,
                        width=18, height=18,
                        border_radius=ft.BorderRadius.all(9),
                        alignment=ft.Alignment(0, 0),
                        right=0, top=0,
                        shadow=ft.BoxShadow(
                            spread_radius=0, blur_radius=8,
                            color=ft.Colors.with_opacity(0.6, DANGER),
                        ),
                    ),
                ]),
            ],
        ),
    )

    content_area = ft.Container(ref=content_area_ref, content=catalog_panel, expand=True)
    page.add(ft.Column(controls=[header, tab_bar, content_area], expand=True, spacing=0))
    page.update()





if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
