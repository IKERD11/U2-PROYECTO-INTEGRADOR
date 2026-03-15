import flet as ft
from main import main

if __name__ == "__main__":
    ft.app(
        target=main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER,
        port=8080,
        host="0.0.0.0"
    )
