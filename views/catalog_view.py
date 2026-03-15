import flet as ft
from components.product_card import build_product_card

# ── Dark Mode Tokens ───────────────────────────────────────────────
BG        = "#0B0F19"
SURFACE   = "#1A2235"
PRIMARY   = "#3B82F6"
TEXT_MAIN = "#F8FAFC"
TEXT_SUB  = "#94A3B8"

CAT_COLORS = {
    "Todas": "#475569", "Wearables": "#8B5CF6",
    "Audio": "#F97316", "Periféricos": "#3B82F6",
    "Monitores": "#06B6D4", "Portátiles": "#DB2777",
    "Gaming": "#7C3AED", "Fotografía": "#EC4899",
    "Almacenamiento": "#6366F1", "PC": "#2563EB",
    "Redes": "#10B981", "Accesorios": "#F59E0B",
}

SORT_OPTIONS = [
    ft.dropdown.Option("name_asc",   "Nombre A→Z"),
    ft.dropdown.Option("name_desc",  "Nombre Z→A"),
    ft.dropdown.Option("price_asc",  "Menor Precio"),
    ft.dropdown.Option("price_desc", "Mayor Precio"),
    ft.dropdown.Option("rating_desc","Mejor Valorados"),
]

_FIELD_STYLE = dict(
    bgcolor="#1E293B", color=TEXT_MAIN,
    hint_style=ft.TextStyle(color=TEXT_SUB, size=14),
    border_color="transparent", focused_border_color=PRIMARY,
    border_radius=12, border_width=1,
    content_padding=ft.Padding.symmetric(horizontal=16, vertical=12),
)

def _build_sort_dropdown(on_change_fn):
    dd = ft.Dropdown(
        options=SORT_OPTIONS, value="name_asc", expand=True,
        bgcolor="#1E293B", color=TEXT_MAIN, border_color="transparent",
        border_radius=12, border_width=1,
        text_size=14,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=0),
    )
    dd.on_change = on_change_fn
    return dd

def build_catalog_panel(page, state, all_products, on_add_to_cart, on_toggle_fav, on_view_detail):
    fs = {"search": "", "min": 0.0, "max": 99999.0, "sort": "name_asc", "cat": "Todas"}
    grid_ref  = ft.Ref[ft.Row]()
    chips_ref = ft.Ref[ft.Row]()
    categories = ["Todas"] + sorted(list(set(p.category for p in all_products)))

    def get_filtered():
        products = list(all_products)
        if fs["cat"] != "Todas": products = [p for p in products if p.category == fs["cat"]]
        q = fs["search"].strip().lower()
        if q: products = [p for p in products if q in p.name.lower() or q in p.description.lower()]
        products = [p for p in products if fs["min"] <= p.price <= fs["max"]]
        sort_map = {
            "name_asc":   (lambda p: p.name.lower(), False),
            "name_desc":  (lambda p: p.name.lower(), True),
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
                    [ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, size=64, color="#E2E8F0"),
                     ft.Text("No encontramos lo que buscas", size=18, color=TEXT_SUB, weight=ft.FontWeight.W_500)],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                alignment=ft.Alignment(0, 0), width=1000, height=400,
            )]
        else:
            grid_ref.current.controls = [
                build_product_card(p, state, on_add_to_cart, on_toggle_fav, on_view_detail)
                for p in products
            ]
        page.update()

    def make_chips():
        chips = []
        for cat in categories:
            active = fs["cat"] == cat
            cat_color = CAT_COLORS.get(cat, PRIMARY)
            
            def click_fn(c=cat):
                def on_click(e):
                    fs["cat"] = c
                    chips_ref.current.controls = make_chips()
                    refresh_grid()
                return on_click

            chips.append(ft.Container(
                content=ft.Text(
                    cat, size=13, 
                    color="#FFF" if active else TEXT_MAIN, 
                    weight=ft.FontWeight.W_700 if active else ft.FontWeight.W_500
                ),
                bgcolor=cat_color if active else SURFACE,
                border_radius=10,
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                border=ft.Border.all(1, cat_color if active else "#334155"),
                ink=True, on_click=click_fn(),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT)
            ))
        return chips

    def on_search(e): fs["search"] = e.control.value; refresh_grid()
    def on_sort(e): fs["sort"] = e.control.value; refresh_grid()
    def on_min(e):
        try: fs["min"] = float(e.control.value) if e.control.value else 0.0
        except: fs["min"] = 0.0
        refresh_grid()
    def on_max(e):
        try: fs["max"] = float(e.control.value) if e.control.value else 99999.0
        except: fs["max"] = 99999.0
        refresh_grid()

    filter_bar = ft.Container(
        bgcolor=SURFACE, border_radius=16, padding=ft.Padding.symmetric(horizontal=16, vertical=20), 
        margin=ft.Margin.only(bottom=20),
        border=ft.Border.all(1, "#1E293B"),
        content=ft.Column(spacing=16, controls=[
            ft.Row([
                ft.TextField(hint_text="Buscar...", prefix_icon=ft.Icons.SEARCH_ROUNDED,
                             on_change=on_search, expand=True, **_FIELD_STYLE),
                _build_sort_dropdown(on_sort),
            ], spacing=10, wrap=True),
            ft.Row([
                ft.Column([
                    ft.Text("PRECIO", size=11, weight=ft.FontWeight.W_800, color=TEXT_SUB),
                    ft.Row([
                        ft.TextField(hint_text="Min", on_change=on_min, width=75, **_FIELD_STYLE),
                        ft.Text("—", color="#CBD5E1", weight=ft.FontWeight.BOLD),
                        ft.TextField(hint_text="Max", on_change=on_max, width=75, **_FIELD_STYLE),
                    ], spacing=8),
                ], spacing=8),
                ft.Row(ref=chips_ref, controls=make_chips(), spacing=8, wrap=True, expand=True),
            ], spacing=16, wrap=True),
        ]),
    )

    grid = ft.ResponsiveRow(ref=grid_ref, spacing=20, run_spacing=20, alignment=ft.MainAxisAlignment.START, controls=[
        build_product_card(p, state, on_add_to_cart, on_toggle_fav, on_view_detail) for p in get_filtered()
    ])

    return ft.Container(
        expand=True, padding=ft.Padding.symmetric(horizontal=20, vertical=30),
        content=ft.Column([grid], scroll=ft.ScrollMode.HIDDEN, expand=True)
    ), refresh_grid
