# Catálogo de Productos TechStore 🛒

Este proyecto es una aplicación interactiva desarrollada en Python utilizando el moderno framework **Flet**. La aplicación simula una tienda en línea (TechStore) donde los usuarios pueden visualizar productos, agregarlos a un carrito de compras y marcarlos como favoritos.

🌍 **Enlace al proyecto:** [https://productoscat.netlify.app/](https://productoscat.netlify.app/)

## 🚀 Características Principales

- **Catálogo Dinámico:** Visualización atractiva de los productos con imágenes, precios y detalles.
- **Carrito de Compras:** Sistema para agregar, incrementar, disminuir o eliminar productos del carrito, con cálculo automático del total.
- **Favoritos:** Posibilidad de marcar y desmarcar productos como favoritos.
- **Diseño Responsivo:** Adaptable tanto a dispositivos móviles como a pantallas de escritorio. Cuenta con un diseño elegante basado en un tema oscuro (Dark Theme).
- **Manejo de Estado (State Management):** Uso de clases para mantener centralizado el estado global de la aplicación.

---

## 🏗️ Arquitectura y Estructura del Código

El proyecto sigue una arquitectura modular y organizada, separando el código en distintas responsabilidades para hacerlo más mantenible:

### 1. Punto de Entrada (`main.py`)
Es el punto de entrada principal. Se encarga de inicializar la página, definir el tema visual (modo oscuro), y construir la interfaz con todos sus componentes. También gestiona la lógica de diálogos y pop-ups.
```python
import flet as ft
from state.app_state import AppState

def main(page: ft.Page):
    page.title = "TechStore — Premium Experience"
    page.bgcolor = "#0B0F19" # Fondo principal Dark Theme
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    
    # Manejador de estado global de la app
    state = AppState()
    # ... Resto de la lógica UI con Flet
```

### 2. Modelo de Datos (`models/product.py`)
Define la estructura de datos para un artículo tecnológico utilizando `dataclasses` para una generación automática y limpia de constructores.
```python
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
```

### 3. Estado de la Aplicación (`state/app_state.py`)
Controla la lógica de negocio y almacena la información que cambia dinámicamente durante el uso de la app. Gestiona centralmente el carrito de compras y los productos favoritos para que todo componente visual interactúe con el mismo origen de datos.
```python
class AppState:
    """Estado global compartido: carrito y favoritos."""
    def __init__(self):
        self.cart: dict[int, dict] = {}   # Guarda el artículo y la cantidad
        self.favorites: set[int] = set()  # IDs de productos favoritos

    def add_to_cart(self, product):
        pid = product.id
        if pid in self.cart:
            self.cart[pid]["qty"] += 1
        else:
            self.cart[pid] = {"product": product, "qty": 1}

    def toggle_favorite(self, pid: int):
        if pid in self.favorites:
            self.favorites.discard(pid)
        else:
            self.favorites.add(pid)
```

### 4. Vistas y Componentes Reutilizables (`views/` y `components/`)
El aspecto visual de Flet se encapsula en funciones reutilizables que construyen contenedores dinámicos, adaptándose a la información proporcionada.

#### Tarjeta de Producto (`components/product_card.py`)
Construye la tarjeta visual para cada ítem del catálogo, permitiendo interacciones (favorito, carrito y vista detalle).
```python
def build_product_card(product: Product, state, on_add_to_cart, on_toggle_fav, on_view_detail):
    is_fav = state.is_favorite(product.id)
    in_stock = product.stock > 0

    return ft.Container(
        # Comportamiento Responsivo 
        col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
        bgcolor="#1A2235",
        border_radius=16,
        on_click=lambda e: on_view_detail(product),
        content=ft.Column(
            controls=[
                ft.Image(src=product.image_path, fit=ft.BoxFit.COVER),
                ft.Text(product.name, size=16, weight=ft.FontWeight.W_700),
                # Y los botones respectivos...
            ]
        )
    )
```

#### Panel Principal / Catálogo (`views/catalog_view.py`)
Genera la grilla de productos y gestiona su sistema de filtrado avanzado, como búsqueda y rango de precio.
```python
def build_catalog_panel(page, state, all_products, on_add_to_cart, on_toggle_fav, on_view_detail):
    # Diccionario de estado interno de búsqueda
    fs = {"search": "", "min": 0.0, "max": 99999.0, "sort": "name_asc", "cat": "Todas"}
    
    def get_filtered():
        # Lógica para filtrar y mapear cada producto
        products = list(all_products)
        if fs["cat"] != "Todas": 
            products = [p for p in products if p.category == fs["cat"]]
        # ...Más lógicas de filtro por precio y texto...
        return products

    # Retorna un agrupador o 'Grid' Responsivo
    return ft.Container(
        content=ft.Column([
            ft.ResponsiveRow(controls=[
               build_product_card(p, state, ...) for p in get_filtered()
            ])
        ])
    ), refresh_grid
```

#### Panel de Favoritos (`views/favorites_view.py`)
Es similar al catálogo, pero filtra únicamente aquellos que se encuentran en el conjunto `state.favorites`.
```python
def build_favorites_panel(page, state, all_products, on_add_to_cart, on_toggle_fav, on_view_detail):
    
    def refresh_favs():
        fav_ids  = state.get_favorites()
        products = [p for p in all_products if p.id in fav_ids]

        if not products:
            # Mensaje cuando está vacío
            grid_ref.current.controls = [ft.Text("Aún no tienes favoritos")]
        else:
            # Reutilizando el componente Card
            grid_ref.current.controls = [
                build_product_card(p, ...) for p in products
            ]
            
    # Retorna el componente y su disparador de recarga
    return ft.Container(...), refresh_favs
```

### 5. Controladores Especiales
- **`data/repository.py`**: Proporciona la base de datos simulada mediante una lista en memoria.
```python
def get_products() -> list[Product]:
    return [
        Product(
            id=1, name="Smartwatch Pro X",
            description="Reloj inteligente con monitor de ritmo...",
            price=199.99, image_path="smartwatch.png", category="Wearables",
        ),
        # ... más productos
    ]
```
- **`generate_qr.py`**: Un pequeño script en python que mediante `qrcode` genera una imagen QR dirigiendo automáticamente hacia [https://productoscat.netlify.app/](https://productoscat.netlify.app/).

---

## 📚 Librerías Utilizadas

El proyecto utiliza distintas librerías declaradas en el archivo `requirements.txt`:

1. **[Flet](https://flet.dev/)**: 
   Es la tecnología principal del proyecto. Flet es un framework que permite crear aplicaciones web, de escritorio y móviles interactivas en Python sin necesidad de escribir código en frontend (HTML, CSS o JavaScript). Utiliza Flutter bajo el capó para renderizar las interfaces.

2. **[qrcode](https://pypi.org/project/qrcode/)**:
   Una librería utilizada para la creación de códigos QR. En el proyecto se usa para generar un código que los usuarios puedan escanear con la cámara y acceder directamente a la aplicación (script `generate_qr.py`).

3. **[Pillow](https://python-pillow.org/)**:
   Es la biblioteca estándar de procesamiento de imágenes en Python (fork de PIL). Trabaja en conjunto con la librería `qrcode` para crear o manipular la imagen del archivo QR final.

## 🛠️ Cómo Ejecutar el Proyecto Localmente

Para correr la aplicación en tu computadora, sigue estos pasos:

1. Clona o descarga este repositorio.
2. Abre una terminal y navega hasta la carpeta del proyecto.
3. Se recomienda crear un entorno virtual e instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el archivo principal:
   ```bash
   python main.py
   ```
   *Alternativamente, puedes usar `root_web.py` o `run_mobile.py` dependiendo del entorno que quieras probar.*

---
¡Gracias por visitar el proyecto! Explora el código y prueba la tienda funcional en el [enlace oficial](https://productoscat.netlify.app/).