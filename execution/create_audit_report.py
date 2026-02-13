
import os
import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # c:/.../audit toko external shopee/
TEMPLATE_DIR = os.path.join(BASE_DIR, 'execution', 'templates')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_report(data):
    """
    Generates an HTML report from the template.
    
    Args:
        data (dict): Dictionary containing report data.
    """
    # Load template
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template('report_template.html')
    
    # Add timestamps if not present
    if 'audit_date' not in data:
        data['audit_date'] = datetime.now().strftime("%d %B %Y")
        
    # Render template
    html_content = template.render(**data)
    
    # Save output
    output_filename = f"Audit_Report_{data.get('shop_name', 'Shop').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.html"
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Report generated successfully: {output_path}")
    return output_path

if __name__ == "__main__":
    # Sample Test Data
    sample_data = {
        "shop_name": "Toko Sejahtera Abadi",
        "audit_period": "Februari 2026",
        "products": [
            {
                "name": "Kemeja Flannel Pria Premium - Kotak Merah - Lengan Panjang",
                "sku": "KMJ-FL-RED-001",
                "image_url": "https://dummyimage.com/400x400/7f13ec/ffffff&text=Kemeja+Flannel",
                "title_ok": True,
                "desc_ok": True,
                "video_ok": True,
                "notes": "Good job! Struktur judul dan deskripsi sudah sangat lengkap."
            },
            {
                "name": "Sepatu Lari Wanita",
                "sku": "SPT-RUN-W-02",
                "image_url": "https://dummyimage.com/400x400/ff7f50/ffffff&text=Sepatu+Lari",
                "title_ok": False,
                "desc_ok": False,
                "video_ok": False,
                "notes": "CRITICAL: Judul terlalu pendek. Gunakan rumus: Brand + Kategori + Model. Deskripsi tidak ada size chart."
            },
            {
                "name": "TWS Bluetooth Earphones 5.0 - Noise Cancelling - Putih",
                "sku": "AUD-TWS-WHT",
                "image_url": "https://dummyimage.com/400x400/2ecc71/ffffff&text=TWS+Earbuds",
                "title_ok": True,
                "desc_ok": False,
                "video_ok": True,
                "notes": "Judul sudah oke. Deskripsi kurang info tentang garansi dan kelengkapan box."
            },
            {
                "name": "Serum Wajah Vitamin C 20ml",
                "sku": "BTY-SER-VITC",
                "image_url": "", # Missing image test
                "title_ok": False,
                "desc_ok": True,
                "video_ok": False,
                "notes": "Judul kurang spesifik (missing brand name). Foto produk utama tidak terload."
            },
            {
                "name": "Tas Ransel Laptop Waterproof Anti Maling dengn USB Port - Hitam",
                "sku": "BAG-LPT-BLK-09",
                "image_url": "https://dummyimage.com/400x400/34495e/ffffff&text=Tas+Laptop",
                "title_ok": True,
                "desc_ok": True,
                "video_ok": True,
                "notes": "-"
            },
             {
                "name": "Gamis Syari Wanita Muslimah Modern Kekinian Bahan Premium",
                "sku": "FAS-MUS-GMS-01",
                "image_url": "https://dummyimage.com/400x400/e74c3c/ffffff&text=Gamis+Syari",
                "title_ok": False,
                "desc_ok": True,
                "video_ok": False,
                "notes": "Judul terindikasi spamming keyword 'Kekinian', 'Modern', 'Premium'. Sederhanakan."
            },
            {
                "name": "Kacamata Hitam Polarized Anti UV400 - Frame Matel",
                "sku": "ACC-GLS-BLK",
                "image_url": "https://dummyimage.com/400x400/3498db/ffffff&text=Kacamata",
                "title_ok": True,
                "desc_ok": True,
                "video_ok": True,
                "notes": "Produk sudah optimal."
            },
            {
                "name": "Mouse Gaming Wireless Silent Click Rechargeable",
                "sku": "GAM-MSE-WRL",
                "image_url": "https://dummyimage.com/400x400/9b59b6/ffffff&text=Mouse+Gaming",
                "title_ok": True,
                "desc_ok": False,
                "video_ok": True,
                "notes": "Deskripsi kurang spesifikasi DPI dan battery life."
            },
            {
                "name": "Masker Wajah Aloe Vera Soothing Gel 99%",
                "sku": "BTY-MSK-ALOE",
                "image_url": "https://dummyimage.com/400x400/27ae60/ffffff&text=Aloe+Gel",
                "title_ok": False,
                "desc_ok": True,
                "video_ok": False,
                "notes": "Judul kurang spesifik brand. Foto produk perlu lebih jelas."
            },
            {
                "name": "Dompet Kulit Pria Asli - Coklat Muda",
                "sku": "FAS-WAL-BRN",
                "image_url": "https://dummyimage.com/400x400/d35400/ffffff&text=Dompet",
                "title_ok": True,
                "desc_ok": True,
                "video_ok": False,
                "notes": "Tambahkan video produk untuk meningkatkan konversi."
            }
        ]
    }
    
    try:
        generate_report(sample_data)
    except Exception as e:
        print(f"Error generating report: {e}")
