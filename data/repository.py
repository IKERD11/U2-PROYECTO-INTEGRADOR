from models.product import Product


def get_products() -> list[Product]:
    """Retorna catálogo completo de productos tecnológicos."""
    return [
        # ── Originales ────────────────────────────────────────────
        Product(
            id=1, name="Smartwatch Pro X",
            description="Reloj inteligente con monitor de ritmo cardíaco, GPS integrado, resistencia al agua IP68 y batería de 7 días.",
            price=199.99, image_path="prod1.jpg",
            category="Wearables", stock=5, rating=4.5,
        ),
        Product(
            id=2, name="Auriculares Noise Canceling",
            description="Audífonos Bluetooth over-ear con cancelación activa de ruido, 30h de autonomía y sonido Hi-Fi premium.",
            price=249.50, image_path="prod2.jpg",
            category="Audio", stock=3, rating=4.8,
        ),
        Product(
            id=3, name="Teclado Mecánico RGB",
            description="Teclado gaming con switches rojos, retroiluminación RGB personalizable y cuerpo de aluminio CNC.",
            price=89.90, image_path="prod3.jpg",
            category="Periféricos", stock=12, rating=4.2,
        ),
        Product(
            id=4, name="Ratón Inalámbrico Ergonómico",
            description="Mouse de alta precisión, diseño vertical ergonómico, sensor de 4000 DPI y batería de larga duración.",
            price=45.00, image_path="prod4.jpg",
            category="Periféricos", stock=0, rating=3.9,
        ),
        Product(
            id=5, name='Monitor UltraWide 34"',
            description='Pantalla curva 4K de 34", ideal para productividad y entretenimiento, con soporte HDR10 y 144Hz.',
            price=499.00, image_path="prod5.jpg",
            category="Monitores", stock=2, rating=4.7,
        ),

        # ── Nuevos ────────────────────────────────────────────────
        Product(
            id=6, name="Laptop Ultrabook Pro 15",
            description="Portátil ultradelgado con procesador i9 de 13ª gen, 32GB RAM, SSD 1TB NVMe y pantalla OLED 120Hz.",
            price=1299.00, image_path="prod1.jpg",
            category="Portátiles", stock=4, rating=4.9,
        ),
        Product(
            id=7, name="Auriculares Gaming 7.1",
            description="Sonido envolvente 7.1 virtual, micrófono retráctil con cancelación de ruido y LEDs RGB personalizables.",
            price=79.99, image_path="prod2.jpg",
            category="Gaming", stock=8, rating=4.3,
        ),
        Product(
            id=8, name="Cámara Mirrorless 4K",
            description="Sensor APS-C de 26MP, grabación 4K a 60fps, estabilización óptica de 5 ejes y 25 puntos de enfoque.",
            price=899.00, image_path="prod3.jpg",
            category="Fotografía", stock=2, rating=4.7,
        ),
        Product(
            id=9, name="SSD NVMe 2TB",
            description="Unidad de estado sólido PCIe 4.0 con velocidades de lectura de 7000 MB/s. Compatible con PS5 y PC.",
            price=139.99, image_path="prod4.jpg",
            category="Almacenamiento", stock=20, rating=4.6,
        ),
        Product(
            id=10, name="Tablet Gráfica Pro",
            description="Tableta de dibujo A4 con 8192 niveles de presión, pantalla IPS 2K integrada y lápiz inalámbrico.",
            price=349.00, image_path="prod5.jpg",
            category="Periféricos", stock=6, rating=4.4,
        ),
        Product(
            id=11, name="GPU RTX 5080 Ti",
            description="Tarjeta gráfica de última generación con 16GB GDDR7, soporte raytracing 4.0 y DLSS 4 Ultra.",
            price=1099.00, image_path="prod1.jpg",
            category="PC", stock=1, rating=5.0,
        ),
        Product(
            id=12, name="Router Wi-Fi 6E Tri-Band",
            description="Cobertura de hasta 350m², velocidad de 9.6 Gbps, 8 antenas y soporte para +200 dispositivos simultáneos.",
            price=229.99, image_path="prod2.jpg",
            category="Redes", stock=7, rating=4.5,
        ),
        Product(
            id=13, name="Altavoz Bluetooth 360°",
            description="Sonido omnidireccional de 40W, resistencia al agua IPX7, 24h de autonomía y luz ambiental LED RGB.",
            price=119.00, image_path="prod3.jpg",
            category="Audio", stock=10, rating=4.2,
        ),
        Product(
            id=14, name="Cargador Inalámbrico 65W",
            description="Carga rápida Qi2 de 65W, compatible con iPhone, Android y AirPods. Carga 3 dispositivos a la vez.",
            price=59.99, image_path="prod4.jpg",
            category="Accesorios", stock=15, rating=4.0,
        ),
        Product(
            id=15, name="Banda Fitness Pro 5",
            description="Monitor de salud 24/7 con ECG, SpO2, GPS integrado, pantalla AMOLED y batería de 14 días.",
            price=169.00, image_path="prod5.jpg",
            category="Wearables", stock=0, rating=4.3,
        ),
    ]
