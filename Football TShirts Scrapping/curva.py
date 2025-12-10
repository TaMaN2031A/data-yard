import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import yagmail
import datetime as dt
import os
import time

# -------------------- SCRAPER --------------------
def scrapper():
    URL = "https://curvaegypt.com/about/top-products"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    all_products_data = []
    MAX_PAGES_TO_SCRAPE = 3

    driver.get(URL)

    for page_num in range(1, MAX_PAGES_TO_SCRAPE + 1):
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return Object.values(window.__NUXT__.data).length") > 0
        )
        products_list = driver.execute_script("return Object.values(window.__NUXT__.data)[0].data.data;")
        if products_list:
            for product in products_list:
                is_available = product.get("availability") == "available"
                has_discount = product.get("offer_ratio") is not None
                all_products_data.append({
                    "name": product.get("name"),
                    "original price": product.get("init_price"),
                    "discount": has_discount,
                    "discounted price": product.get("offer_price"),
                    "available": is_available
                })
        if page_num < MAX_PAGES_TO_SCRAPE:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Go to next page']"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)

    driver.quit()
    df = pd.DataFrame(all_products_data)
    return df

# -------------------- WRITER --------------------
def writer(df):
    service_account_json = os.environ.get("GOOGLE_KEY_JSON")
    with open("key.json", "w") as f:
        f.write(service_account_json)

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file("key.json", scopes=scopes)
    client = gspread.authorize(creds)

    today_ss = client.open("Curva Today Market State")
    today_sheet = today_ss.get_worksheet(0)
    today_sheet.clear()
    set_with_dataframe(today_sheet, df)

    archive_ss = client.open("Curva Market Day-to-Day State")
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

# -------------------- EMAIL --------------------
def email_notifier():
    app_password = os.environ.get("EMAIL_APP_PASSWORD")
    sender_email = "tamanabdullah9@gmail.com"
    receiver_email = "ramyalimahmoud@gmail.com"
    today_str = dt.datetime.now().strftime("%Y-%m-%d (%A)")
    message = f"""سلام عليكم ورحمة الله وبركاته
صباحو يابو الريم
هذا ايميل تلقائي
تم إضافة بيانات اليوم لموقع كورفا
اليوم: {today_str}
"""
    yag = yagmail.SMTP(sender_email, app_password)
    yag.send(
        to=receiver_email,
        subject="تحديث بيانات كورفا — إرسال تلقائي",
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
