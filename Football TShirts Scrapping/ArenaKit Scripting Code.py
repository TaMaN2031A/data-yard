import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen

def scrapper():

    def find_products_in_html():
        url = "https://arenakit.net/shop"
        page = urlopen(url)
        html_bytes = page.read()
        html = html_bytes.decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        required_element = None
        print(soup)
        for i in soup.descendants:
            if i.getText().count("{\"state\":{\"data\":{\"products\":") != 0:
                required_element = i

        if required_element == None:
            raise "Element Not Found"
        raw_text = required_element.getText()
        print(required_element)

        start_index = raw_text.find('{"state":{"data":{"products":')
        if start_index == -1:
            raise ValueError("لم يتم العثور على بداية JSON المطلوبة")

        json_part = raw_text[start_index:]

        brace_count = 0
        end_index = None
        for i, ch in enumerate(json_part):
            if ch == '{':
                brace_count += 1
            elif ch == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_index = i + 1
                    break

        if end_index is None:
            raise ValueError("لم يتم العثور على نهاية JSON")

        clean_json = json_part[:end_index]

        data = json.loads(clean_json)

        products = data["state"]["data"]["products"]
        print(products)
        return products

    def extract_variants_per_row(products):
        rows = []
        for p in products:
            name = p.get("name", "")
            size_names = []
            for opt in p.get("productOptions", []):
                if 'size' in (opt.get("name") or "").lower() or 'size' in (
                        opt.get("option", {}).get("name") or "").lower():
                    size_names = opt.get("values", []) or []
                    break
            variants = p.get("variants", [])
            for i, var in enumerate(variants):
                size = size_names[i] if i < len(size_names) else var.get("sku") or f"Variant {i + 1}"
                available = (var.get("quantity", 0) > 0)
                waiting = len(var.get("notifyInStockList", []) or [])
                price_cents = var.get("priceCents")
                if price_cents is None:
                    price_cents = p.get("priceCents", 0)
                price = price_cents / 100 if price_cents is not None else None
                disc_cents = var.get("discountedPriceCents")
                if disc_cents is None:
                    disc_cents = p.get("discountedPriceCents", 0)
                discounted_price = (disc_cents or 0) / 100 if disc_cents is not None else None
                has_discount = False
                if discounted_price and price is not None:
                    has_discount = discounted_price < price
                on_sale = var.get("isOnSale", p.get("isOnSale", False))
                rows.append({
                    "name": name,
                    "size": size,
                    "available": available,
                    "waiting": waiting,
                    "price": price,
                    "on_sale": on_sale,
                    "discounted_price": discounted_price if has_discount else None,
                })
        return pd.DataFrame(rows)

    df = extract_variants_per_row(find_products_in_html())
    print(df)
    df.sort_values(by=["waiting", "price"], ascending=[False, True], inplace=True)
    return df

def writer(df):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file("key.json", scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open("Playground").sheet1
    print("Writing to Google Sheet")
    set_with_dataframe(sheet, df)

writer(scrapper())