import gspread
from google.oauth2.service_account import Credentials

# الصلاحيات
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# قراءة credentials
creds = Credentials.from_service_account_file("key.json", scopes=scopes)

# الاتصال بـ gspread
client = gspread.authorize(creds)

# فتح Sheet
sheet = client.open("Playground").sheet1  # الورقة الأولى

# كتابة نص
sheet.update_acell("A1", "Hello from Python!")

# إضافة صف كامل
sheet.append_row(["Name", "Age", "City"])
