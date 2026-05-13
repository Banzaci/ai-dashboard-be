import pandas as pd
import csv

BASE_DIR = './'

df = pd.read_csv(BASE_DIR + 'data.csv')

df["name"] = (
    df["name"]
    .str.replace(r"\s+", "", regex=True)
    .str.strip()
    .str.capitalize()
)

print(df["city"])

# with open(BASE_DIR + 'data.csv', 'r') as f:
#     reader = csv.reader(f)
#     data = list(reader)

# df = pd.DataFrame(data[1:], columns=data[0])
# print(df)