import scrap
import pandas as pd
import datetime

today = str(datetime.datetime.now()+datetime.timedelta(hours = 8)).split(' ')[0]

all_stock_code = list(pd.read_csv('https://storage.googleapis.com/hedgefund/Mainboard%20List.csv').TICKER)
c = scrap.ccass()

all_tables = []
for i in all_stock_code:
  try:
    print(i)
    all_tables.append(c.get_table(i))
  except:
    ''
df = pd.concat(all_tables)

df.to_csv('/home/yinpatt/ccass_raw/daily/main_df/main_df_'+str(today)+'.csv', index = False)
