import requests

# Supabase configuration
SUPABASE_URL = 'https://zsskdgkqlcuwwarlqwsz.supabase.co'
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpzc2tkZ2txbGN1d3dhcmxxd3N6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg0MDQ3NzIsImV4cCI6MjA4Mzk4MDc3Mn0.BkrK1Hbg2K5Q6D_UxI9BBAF-g1W6bvgdxhUEiv205uA'

def fetch_products():
    """Fetch products from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/products"
    headers = {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
        'Content-Type': 'application/json'
    }
    params = {
        'select': 'product_code,product_name,in_house_name',
        'order': 'in_house_name.asc'
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def format_for_email(products):
    """Format products as simple list for email"""
    lines = []

    lines.append("PACKAGING PRODUCTS LIST")
    lines.append("")
    lines.append("Product Code | In-House Name | Product Name")
    lines.append("")

    for product in products:
        code = product.get('product_code') or '-'
        name = product.get('product_name') or '-'
        in_house = product.get('in_house_name') or '-'

        lines.append(f"{code} | {in_house} | {name}")

    lines.append("")
    lines.append(f"Total: {len(products)} products")

    return "\n".join(lines)

def main():
    print("Fetching products from Supabase...")
    products = fetch_products()

    if not products:
        print("No products found.")
        return

    print(f"Found {len(products)} products.\n")

    # Format and display
    email_text = format_for_email(products)
    print(email_text)

    # Also save to file
    output_file = "products_export.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(email_text)
    print(f"\nSaved to {output_file}")

if __name__ == "__main__":
    main()
