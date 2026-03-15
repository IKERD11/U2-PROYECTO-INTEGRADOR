import os
import flet as ft
from main import main

if __name__ == "__main__":
    # Set the environment variable to trigger mobile mode in main.py
    os.environ["FLET_MOBILE"] = "True"
    
    # Run the application
    # Note: We use assets_dir="assets" to match the original execution
    ft.app(target=main, assets_dir="assets")
