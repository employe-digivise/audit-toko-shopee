# Create Audit Report

This directive outlines the process for generating a standardized HTML Audit Report for Shopee stores, including functionality to save as PDF.

## Goal
Generate a professional, branded HTML report that summarizes audit findings, specifically focusing on Product Title (SEO) and Description Content.

## Tools
- `execution/create_audit_report.py`

## Data Structure
The `sample_data` dictionary in `execution/create_audit_report.py` must include:
- `shop_name`
- `audit_period`
- `products`: List of dictionaries, each containing:
    - `name`
    - `sku`
    - `image_url`
    - `title_ok` (Boolean)
    - `desc_ok` (Boolean)
    - `video_ok` (Boolean) - *New*: Determines presence in "Top Products: Video Presence".
    - `notes`

## Report Layout Specification
1.  **Header**: Shop info and floating PDF download button (hidden in PDF).
2.  **Metrics Grid**: 3 cards (Total Products, Voucher Status, Compliance Score).
3.  **Top Products: Video Presence**:
    -   Grid of **exactly 10 items**.
    -   Shows thumbnail, truncated name, and status (VIDEO OK / MISSING).
4.  **Detail Audit: Best Selling Product**:
    -   **Page Break Before** this section.
    -   Displays details for **only 1 product** (the first in the list).
    -   Includes Audit Notes and Content Check.
5.  **Detail Kelengkapan Foto Produk**:
    -   Checklist of visual criteria (Manfaat, Aksen, Kontras, Detail).
    -   3x3 Grid of sample generic images.
6.  **Audit Criteria Reference**:
    -   Moved to the bottom of the report.
7.  **Footer**: Generation timestamp.

## Execution
Run the script to generate the HTML report in the `outputs/` directory.
```bash
python execution/create_audit_report.py
```
3. The script will render `execution/templates/report_template.html`.
4. Output will be saved to `outputs/Audit_Report_[ShopName]_[Date].html`.

## Outputs
- **Result**: An HTML file in `outputs/`.
- **Action**: Open the HTML file in a browser and click "Download PDF" to save the final document.

## Edge Cases
- **Missing Images**: Template handles empty image URLs gracefully.
- **Long Titles**: CSS clamps text to 2 lines in the preview card.
