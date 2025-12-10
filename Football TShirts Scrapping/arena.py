import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime as dt
import pandas as pd
import json
import yagmail
import os

# -------------------- SCRAPER FUNCTION --------------------
def scrapper():
    url = "https://arenakit.net/shop"
    html = urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    required_element = None
    for i in soup.descendants:
        if i.getText().count("{\"state\":{\"data\":{\"products\":") != 0:
            required_element = i
            break

    if required_element is None:
        raise ValueError("Element Not Found")

    raw_text = required_element.getText()
    start_index = raw_text.find('{"state":{"data":{"products":')
    if start_index == -1:
        raise ValueError("JSON start not found")

    json_part = raw_text[start_index:]
    brace_count = 0
    end_index = None
    for idx, ch in enumerate(json_part):
        if ch == "{":
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count == 0:
                end_index = idx + 1
                break

    clean_json = json_part[:end_index]
    data = json.loads(clean_json)
    products = data["state"]["data"]["products"]

    rows = []
    for p in products:
        name = p.get("name", "")
        size_names = []

        for opt in p.get("productOptions", []):
            if "size" in (opt.get("name") or "").lower():
                size_names = opt.get("values", [])
                break

        for i, var in enumerate(p.get("variants", [])):
            size = size_names[i] if i < len(size_names) else f"Variant {i+1}"
            price = (var.get("priceCents") or p.get("priceCents", 0)) / 100
            waiting = len(var.get("notifyInStockList", []))
            available = var.get("quantity", 0) > 0

            rows.append({
                "name": name,
                "size": size,
                "available": available,
                "waiting": waiting,
                "price": price
            })

    df = pd.DataFrame(rows)
    df.sort_values(by=["waiting", "price"], ascending=[False, True], inplace=True)
    return df

# -------------------- WRITER FUNCTION --------------------
def writer(df):
    # تحميل JSON من Secrets
    service_account_json = os.environ.get("GOOGLE_KEY_JSON")
    with open("key.json", "w") as f:
        f.write(service_account_json)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file("key.json", scopes=scopes)
    client = gspread.authorize(creds)

    # ---------------- Today Market State ----------------
    today_ss = client.open("Today Market State")
    today_sheet = today_ss.get_worksheet(0)
    today_sheet.clear()
    set_with_dataframe(today_sheet, df)

    # ---------------- Market Day-to-Day State ----------------
    archive_ss = client.open("Market Day-to-Day State")
    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    try:
        day_sheet = archive_ss.worksheet(today_str)
        day_sheet.clear()
    except gspread.WorksheetNotFound:
        day_sheet = archive_ss.add_worksheet(
            title=today_str,
            rows=str(len(df)+10),
            cols=str(len(df.columns)+5)
        )
    set_with_dataframe(day_sheet, df)

# -------------------- EMAIL FUNCTION --------------------
def email_notifier():
    app_password = os.environ.get("EMAIL_APP_PASSWORD")
    sender_email = "tamanabdullah9@gmail.com"
    receiver_email = "ramyalimahmoud@gmail.com"

    today_str = dt.datetime.now().strftime("%Y-%m-%d (%A)")
    message = f"""سلام عليكم ورحمة الله وبركاته
صباحو يابو الريم
هذا ايميل تلقائي
تم إضافة بيانات اليوم لموقع أرينا
اليوم: {today_str}
"""

    yag = yagmail.SMTP(sender_email, app_password)
    yag.send(
        to=receiver_email,
        subject="تحديث بيانات أرينا — إرسال تلقائي",
        contents=message
    )
    print("Email sent successfully!")

# -------------------- RUN PIPELINE --------------------
def run_pipeline():
    df = scrapper()
    writer(df)
    email_notifier()
    print("Pipeline finished successfully!")

if __name__ == "__main__":
    run_pipeline()
