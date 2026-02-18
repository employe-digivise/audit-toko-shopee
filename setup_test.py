import shutil
import os
import json

files_to_copy = [
    "image.png",
    "image copy.png",
    "image copy 2.png",
    "image copy 3.png",
    "image copy 4.png",
    "image copy 5.png",
    "image copy 6.png",
    "image copy 7.png",
    "image copy 8.png"
]

output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

for f in files_to_copy:
    if os.path.exists(f):
        shutil.copy(f, os.path.join(output_dir, f))
        print(f"Copied {f} to {output_dir}")
    else:
        print(f"Warning: {f} not found")

dummy_data = {
    "shop_name": "Toko Variasi Image",
    "audit_period": "Februari 2026",
    "products": [
        {
            "name": "Produk Dengan Variasi Lengkap",
            "sku": "VAR-001",
            "cover_image": "image.png",
            "variation_images": [
                "image copy.png",
                "image copy 2.png",
                "image copy 3.png",
                "image copy 4.png",
                "image copy 5.png",
                "image copy 6.png",
                "image copy 7.png",
                "image copy 8.png"
            ],
            "title_ok": True,
            "desc_ok": True,
            "video_ok": True,
            "notes": "Testing cover and 8 variations."
        }
    ]
}

with open("dummy_data_variations.json", "w") as f:
    json.dump(dummy_data, f, indent=2)
    print("Created dummy_data_variations.json")
