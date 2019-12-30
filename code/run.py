import scrap
import pandas as pd
all_stock_code = list(pd.read_csv('https://storage.googleapis.com/hedgefund/Mainboard%20List.csv').TICKER)
c = scrap.ccass()

all_tables = []
for i in all_stock_code:
  try:
    all_tables.append(c.get_table(i))
  except:
    ''
