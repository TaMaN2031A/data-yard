import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import datetime as dt

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from selenium.webdriver.chrome.options import Options


# -------------------- SCRAPER FUNCTION --------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def scrapper(**kwargs):
    URL = "https://curvaegypt.com/about/top-products"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    all_products_data = []
    MAX_PAGES_TO_SCRAPE = 3

    print("بدء عملية السكرابنج للموقع وتحميل الصفحة الأولى...")
    driver.get(URL)

    for page_num in range(1, MAX_PAGES_TO_SCRAPE + 1):
        print(f"جار استخراج البيانات من الصفحة رقم {page_num}...")

        # انتظر حتى Nuxt data تكون جاهزة
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return Object.values(window.__NUXT__.data).length") > 0
        )

        # جلب البيانات بدون مفتاح ثابت
        js_script = "return Object.values(window.__NUXT__.data)[0].data.data;"
        products_list = driver.execute_script(js_script)

        if products_list:
            for product in products_list:
                is_available = product.get("availability") == "available"
                has_discount = product.get("offer_ratio") is not None

                product_data = {
                    "name": product.get("name"),
                    "original price": product.get("init_price"),
                    "discount": has_discount,
                    "discounted price": product.get("offer_price"),
                    "available": is_available
                }
                all_products_data.append(product_data)

        # الانتقال للصفحة التالية
        if page_num < MAX_PAGES_TO_SCRAPE:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Go to next page']"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)

    driver.quit()

    df = pd.DataFrame(all_products_data)
    # حفظ DataFrame في XCom ليتم استخدامه لاحقًا
    kwargs['ti'].xcom_push(key='curva_market_data', value=df.to_json(orient="split"))


# -------------------- WRITER FUNCTION --------------------
def writer(**kwargs):
    ti = kwargs['ti']
    df_json = ti.xcom_pull(key='curva_market_data', task_ids='scrapper_task')
    df = pd.read_json(df_json, orient="split")

    # ✔ المسار الصحيح داخل WSL
    SERVICE_ACCOUNT_PATH = "/home/eyad/airflow/dags/key.json"

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_PATH, scopes=scopes)
    client = gspread.authorize(creds)

    # ---------------- Today Market State ----------------
    today_ss = client.open("Curva Today Market State")
    today_sheet = today_ss.get_worksheet(0)
    today_sheet.clear()
    set_with_dataframe(today_sheet, df)

    # ---------------- Market Day-to-Day State ----------------
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


# -------------------- AIRFLOW DAG --------------------
default_args = {
    "owner": "airflow",
    "start_date": dt.datetime(2025, 11, 23),
    "retries": 12,
    "retry_delay": dt.timedelta(hours=1),
}

with DAG(
    "OraMarketDagCurva",
    default_args=default_args,
    schedule=dt.timedelta(days=1),
    catchup=False,
) as dag:

    scrapper_task = PythonOperator(
        task_id="scrapper_task",
        python_callable=scrapper,
    )

    writer_task = PythonOperator(
        task_id="writer_task",
        python_callable=writer,
    )

    scrapper_task >> writer_task

# https://docs.google.com/spreadsheets/d/1USsEmczh5G49qV8P8_WQcdOh93Y9eERfQORLF5YNZMU/edit?gid=0#gid=0
# https://docs.google.com/spreadsheets/d/1USsEmczh5G49qV8P8_WQcdOh93Y9eERfQORLF5YNZMU/edit?gid=0#gid=0