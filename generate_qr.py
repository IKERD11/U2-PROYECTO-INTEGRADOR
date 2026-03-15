import qrcode
import os

def generate_qr(url, output_path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(output_path)
    print(f"QR code generated and saved to {output_path}")

if __name__ == "__main__":
    url = "http://172.20.10.2:8080"
    output_path = "assets/mobile_app_qr.png"
    
    # Ensure assets directory exists
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    generate_qr(url, output_path)
