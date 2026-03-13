import flet as ft
from components.product_card import build_product_card

BG      = "#0F172A"
SURFACE = "#1E293B"
PRIMARY = "#6366F1"
TEXT_MAIN = "#F1F5F9"
TEXT_SUB  = "#94A3B8"

CAT_COLORS = {
    "Todas": "#475569", "Wearables": "#7C3AED",
    "Audio": "#EA580C", "Periféricos": "#2563EB",
    "Monitores": "#0D9488", "General": "#475569",
}

SORT_OPTIONS = [
    ft.dropdown.Option("name_asc",   "Nombre A→Z"),
    ft.dropdown.Option("name_desc",  "Nombre Z→A"),
    ft.dropdown.Option("price_asc",  "Precio ↑"),
    ft.dropdown.Option("price_desc", "Precio ↓"),
    ft.dropdown.Option("rating_desc","Rating ↓"),
]

_FIELD_STYLE = dict(
    bgcolor=BG, color=TEXT_MAIN,
    hint_style=ft.TextStyle(color=TEXT_SUB),
    border_color="#334155", focused_border_color=PRIMARY,
    border_radius=10,
    content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
)


def _build_sort_dropdown(on_change_fn):
    """Dropdown de ordenamiento compatible con Flet 0.82.2 (on_change como propiedad)."""
    dd = ft.Dropdown(options=SORT_OPTIONS, value="name_asc", width=160)
    dd.on_change = on_change_fn
    return dd



def build_catalog_panel(page, state, all_products, on_add_to_cart, on_toggle_fav, on_view_detail):
    fs = {"search": "", "min": 0.0, "max": 99999.0, "sort": "name_asc", "cat": "Todas"}
    grid_ref  = ft.Ref[ft.Row]()
    chips_ref = ft.Ref[ft.Row]()
    categories = ["Todas"] + sorted(set(p.category for p in all_products))

    # ── Filtering / sorting ────────────────────────────────────────
    def get_filtered():
        products = all_products[:]
        if fs["cat"] != "Todas":
            products = [p for p in products if p.category == fs["cat"]]
        q = fs["search"].strip().lower()
        if q:
            products = [p for p in products if q in p.name.lower() or q in p.description.lower()]
        products = [p for p in products if fs["min"] <= p.price <= fs["max"]]
        sort_map = {
            "name_asc":   (lambda p: p.name,   False),
            "name_desc":  (lambda p: p.name,   True),
            "price_asc":  (lambda p: p.price,  False),
            "price_desc": (lambda p: p.price,  True),
            "rating_desc":(lambda p: p.rating, True),
        }
        key, rev = sort_map[fs["sort"]]
        products.sort(key=key, reverse=rev)
        return products

    def refresh_grid():
        products = get_filtered()
        if not products:
            grid_ref.current.controls = [ft.Container(
                content=ft.Column(
                    [ft.Icon(ft.Icons.SEARCH_OFF, size=60, color="#334155"),
                     ft.Text("Sin resultados", size=16, color=TEXT_SUB)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment(0, 0), width=700, height=280,
            )]
        else:
            grid_ref.current.controls = [
                build_product_card(p, state, on_add_to_cart, on_toggle_fav, on_view_detail)
                for p in products
            ]

    # ── Chips ──────────────────────────────────────────────────────
    def make_chips():
        chips = []
        for cat in categories:
            active = fs["cat"] == cat
            def click_fn(c=cat):
                def on_click(e):
                    fs["cat"] = c
                    chips_ref.current.controls = make_chips()
                    refresh_grid()
                    page.update()
                return on_click
            chips.append(ft.Container(
                content=ft.Text(cat, size=12, color="#FFF" if active else TEXT_SUB,
                                weight=ft.FontWeight.BOLD if active else ft.FontWeight.NORMAL),
                bgcolor=CAT_COLORS.get(cat, "#475569") if active else "#0F172A",
                border_radius=ft.BorderRadius.all(20),
                padding=ft.Padding.symmetric(horizontal=14, vertical=6),
                border=ft.Border.all(1, CAT_COLORS.get(cat, "#475569")),
                ink=True, on_click=click_fn(),
            ))
        return chips

    # ── Event handlers ─────────────────────────────────────────────
    def on_search(e):
        fs["search"] = e.control.value; refresh_grid(); page.update()

    def on_sort(e):
        fs["sort"] = e.control.value; refresh_grid(); page.update()

    def on_min(e):
        try: fs["min"] = float(e.control.value) if e.control.value else 0.0
        except: fs["min"] = 0.0
        refresh_grid(); page.update()

    def on_max(e):
        try: fs["max"] = float(e.control.value) if e.control.value else 99999.0
        except: fs["max"] = 99999.0
        refresh_grid(); page.update()

    # ── Layout ─────────────────────────────────────────────────────
    filter_bar = ft.Container(
        bgcolor=SURFACE, border_radius=ft.BorderRadius.all(14),
        padding=ft.Padding.all(16), margin=ft.Margin.only(bottom=16),
        content=ft.Column(spacing=12, controls=[
            ft.Row(spacing=12, controls=[
                ft.TextField(hint_text="Buscar producto...", prefix_icon=ft.Icons.SEARCH,
                             on_change=on_search, expand=True, **_FIELD_STYLE),
                _build_sort_dropdown(on_sort),
            ]),
            ft.Row(spacing=8, controls=[
                ft.Text("Precio:", color=TEXT_SUB, size=13),
                ft.TextField(hint_text="Mín", on_change=on_min, width=90,
                             keyboard_type=ft.KeyboardType.NUMBER, **_FIELD_STYLE),
                ft.Text("—", color=TEXT_SUB),
                ft.TextField(hint_text="Máx", on_change=on_max, width=90,
                             keyboard_type=ft.KeyboardType.NUMBER, **_FIELD_STYLE),
            ]),
            ft.Row(ref=chips_ref, controls=make_chips(), spacing=8, wrap=True),
        ]),
    )

    grid = ft.Row(
        ref=grid_ref, wrap=True, spacing=20, run_spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[build_product_card(p, state, on_add_to_cart, on_toggle_fav, on_view_detail)
                  for p in get_filtered()],
    )

    panel = ft.Container(
        expand=True, padding=ft.Padding.all(20),
        content=ft.Column(
            controls=[filter_bar, grid],
            scroll=ft.ScrollMode.AUTO, expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )
    return panel, refresh_grid
