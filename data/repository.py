from models.product import Product


def get_products() -> list[Product]:
    """Retorna catálogo completo de productos tecnológicos."""
    return [
        Product(
            id=1, name="Smartwatch Pro X",
            description="Reloj inteligente con monitor de ritmo cardíaco, GPS integrado y batería de 7 días.",
            price=199.99, image_path="smartwatch.png",
            category="Wearables", stock=5, rating=4.5,
        ),
        Product(
            id=2, name="Auriculares Noise Canceling",
            description="Audífonos Bluetooth over-ear con cancelación activa de ruido y sonido Hi-Fi.",
            price=249.50, image_path="headphones.png",
            category="Audio", stock=3, rating=4.8,
        ),
        Product(
            id=3, name="Teclado Mecánico RGB",
            description="Teclado gaming con switches rojos y retroiluminación RGB personalizable.",
            price=89.90, image_path="keyboard.png",
            category="Periféricos", stock=12, rating=4.2,
        ),
        Product(
            id=4, name="Ratón Inalámbrico Ergonómico",
            description="Mouse de alta precisión, diseño vertical ergonómico y sensor de 4000 DPI.",
            price=45.00, image_path="mouse.png",
            category="Periféricos", stock=0, rating=3.9,
        ),
        Product(
            id=5, name='Monitor UltraWide 34"',
            description='Pantalla curva 4K de 34", ideal para productividad, con soporte HDR10.',
            price=499.00, image_path="monitor.png",
            category="Monitores", stock=2, rating=4.7,
        ),
        Product(
            id=6, name="Laptop Ultrabook Pro 15",
            description="Portátil ultradelgado con procesador i9, 32GB RAM y pantalla OLED 120Hz.",
            price=1299.00, image_path="laptop.png",
            category="Portátiles", stock=4, rating=4.9,
        ),
        Product(
            id=7, name="Auriculares Gaming 7.1",
            description="Sonido envolvente 7.1 virtual y micrófono retráctil con cancelación de ruido.",
            price=79.99, image_path="gaming_headset.png",
            category="Gaming", stock=8, rating=4.3,
        ),
        Product(
            id=8, name="Cámara Mirrorless 4K",
            description="Sensor APS-C de 26MP, grabación 4K a 60fps y estabilización óptica.",
            price=899.00, image_path="camera.png",
            category="Fotografía", stock=2, rating=4.7,
        ),
        Product(
            id=9, name="SSD NVMe 2TB",
            description="Unidad de estado sólido PCIe 4.0 con velocidades de lectura de 7000 MB/s.",
            price=139.99, image_path="ssd.png",
            category="Almacenamiento", stock=20, rating=4.6,
        ),
        Product(
            id=10, name="Tablet Gráfica Pro",
            description="Tableta de dibujo con 8192 niveles de presión y pantalla IPS 2K.",
            price=349.00, image_path="tablet.png",
            category="Periféricos", stock=6, rating=4.4,
        ),
        Product(
            id=11, name="GPU RTX 5080 Ti",
            description="Tarjeta gráfica con 16GB GDDR7, soporte raytracing 4.0 y DLSS 4 Ultra.",
            price=1099.00, image_path="gpu.png",
            category="PC", stock=1, rating=5.0,
        ),
        Product(
            id=12, name="Router Wi-Fi 6E Tri-Band",
            description="Cobertura de hasta 350m², velocidad de 9.6 Gbps y soporte para Wi-Fi 6E.",
            price=229.99, image_path="router.png",
            category="Redes", stock=7, rating=4.5,
        ),
        Product(
            id=13, name="Altavoz Bluetooth 360°",
            description="Sonido omnidireccional de 40W, resistencia al agua IPX7 y 24h de autonomía.",
            price=119.00, image_path="speaker.png",
            category="Audio", stock=10, rating=4.2,
        ),
        Product(
            id=14, name="Cargador Inalámbrico 65W",
            description="Carga rápida Qi2 de 65W. Permite cargar hasta 3 dispositivos a la vez.",
            price=59.99, image_path="charger.png",
            category="Accesorios", stock=15, rating=4.0,
        ),
        Product(
            id=15, name="Banda Fitness Pro 5",
            description="Monitor de salud 24/7 con ECG, SpO2 y GPS integrado. 14 días de batería.",
            price=169.00, image_path="fitness_band.png",
            category="Wearables", stock=0, rating=4.3,
        ),
    ]
