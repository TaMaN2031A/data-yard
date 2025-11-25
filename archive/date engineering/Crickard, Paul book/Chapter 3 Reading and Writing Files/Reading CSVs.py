"""
DictReader يسهل التعامل مع الاعمدة؛ يرجع ماب على الشكل الاتي:
row = {'name':'ahmed', 'age':'25', 'city':'cairo'}
بدلا من:
row = ['ahmed', '25', 'cairo']
المكاسب؟ لا تبالي بأماكن الأعمدة؛ اختر ما تريد
"""

import csv
with open('data.csv') as f:
    myReader = csv.DictReader(f) # myReader is iterator
    headers = next(myReader) # moves like iterable
    for row in myReader:
        print(row['name'])