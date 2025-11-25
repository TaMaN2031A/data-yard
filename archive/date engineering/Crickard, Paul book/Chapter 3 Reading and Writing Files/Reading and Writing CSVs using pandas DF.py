import pandas as pd

df = pd.read_csv('data.csv')
print(df.head())

data = {'Name': ['Paul', 'Bob', 'Susan', 'Yolanda'], 'Age': [23, 45, 18, 21]}
df2 = pd.DataFrame(data)
df.to_csv('from_df.csv', index=False)