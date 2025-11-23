import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
import datetime as dt

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
import pandas as pd


# -------------------- SCRAPER FUNCTION --------------------
def scrapper(**kwargs):
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

    # استخراج المتغيرات لكل منتج
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

    # تخزين الـ DataFrame في XCom
    kwargs['ti'].xcom_push(key='market_data', value=df.to_json(orient="split"))


# -------------------- WRITER FUNCTION --------------------
def writer(**kwargs):
    ti = kwargs['ti']
    df_json = ti.xcom_pull(key='market_data', task_ids='scrapper_task')
    df = pd.read_json(df_json, orient="split")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file("key.json", scopes=scopes)
    client = gspread.authorize(creds)

    # فتح الـ spreadsheet
    ss = client.open("Playground")

    # ---------------- Today Market State ----------------
    today_sheet = ss.get_worksheet(0)
    today_sheet.clear()
    set_with_dataframe(today_sheet, df)

    # ---------------- Market Day-to-Day State ----------------
    today_str = dt.datetime.now().strftime("%Y-%m-%d")
    try:
        day_sheet = ss.worksheet(today_str)
        day_sheet.clear()
    except gspread.WorksheetNotFound:
        day_sheet = ss.add_worksheet(title=today_str, rows=str(len(df)+10), cols=str(len(df.columns)+5))

    set_with_dataframe(day_sheet, df)


# -------------------- AIRFLOW DAG --------------------
default_args = {
    "owner": "airflow",
    "start_date": dt.datetime(2025, 11, 23),
    "retries": 12,
    "retry_delay": dt.timedelta(hours=1),
}

with DAG(
    "OraMarketDag",
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

    # ترتيب التنفيذ
    scrapper_task >> writer_task

# https://docs.google.com/spreadsheets/d/1rIYALNFJdNoeydbyQ6oI5vcaCemHZD0XWtcPdKEgAUQ/edit?usp=sharing
# https://docs.google.com/spreadsheets/d/1Mcp3atUT_q2tYDt44J4Q0m5ItyBFoMsIR7rKDaU7kEw/edit?usp=sharing