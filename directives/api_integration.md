# Audit Report API Integration Guideline

This document outlines how external systems (e.g., Lovable, Bubbles, etc.) can integrate with the Audit Report Server to generate deterministic reports.

## Endpoint

**URL**: `http://<server-ip>:1101/api/generate`
**Method**: `POST`
**Content-Type**: `application/json`

## Request Structure

The request body must be a JSON object with the following structure:

```json
{
  "shop_name": "Toko Sejahtera Abadi",
  "audit_period": "Februari 2026",
  "products": [
    {
      "name": "Product Name",
      "sku": "SKU-123",
      "image_url": "https://example.com/image.jpg",
      "title_ok": true,
      "desc_ok": false,
      "video_ok": true,
      "notes": "Specific audit notes for this product."
    }
  ]
}
```

### Field Definitions

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `shop_name` | String | Yes | Name of the shop being audited. |
| `audit_period` | String | No | Period string (e.g. "March 2026"). Defaults to current month if omitted. |
| `products` | Array | Yes | List of product objects (see below). |

**Product Object:**

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | Yes | Full product title. |
| `sku` | String | No | Stock Keeping Unit identifier. |
| `image_url` | String | No | URL to product image. Empty string allows placeholder. |
| `title_ok` | Boolean | Yes | `true` if title meets SEO criteria, else `false`. |
| `desc_ok` | Boolean | Yes | `true` if description is complete, else `false`. |
| `video_ok` | Boolean | Yes | `true` if video exists, else `false`. |
| `notes` | String | No | Audit findings/remarks. |

## Response

**Success (200 OK):**
```json
{
  "status": "success",
  "message": "Report generated successfully",
  "report_url": "http://<server-ip>:1101/view/Audit_Report_Toko_Sejahtera_Abadi_20260218.html",
  "download_url": "http://<server-ip>:1101/download/Audit_Report_Toko_Sejahtera_Abadi_20260218.html"
}
```

**Error (400 Bad Request):**
```json
{
  "status": "error",
  "message": "Missing required field: shop_name"
}
```

## Example Usage (cURL)

```bash
curl -X POST http://localhost:1101/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "shop_name": "Toko Baru",
    "audit_period": "Maret 2026",
    "products": [
      {
        "name": "Contoh Produk",
        "sku": "TST-001",
        "image_url": "",
        "title_ok": true,
        "desc_ok": true,
        "video_ok": false,
        "notes": "Bagus."
      }
    ]
  }'
```
