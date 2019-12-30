import scrap
import pandas as pd
import datetime
from google.cloud import storage

gcs = storage.Client('secret.json')
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

f = StringIO()
df.to_csv(f)
f.seek(0)
gcs.get_bucket('ccass_raw').blob('daily/main_df/main_df_'+str(today)+'.csv').upload_from_file(f, content_type='text/csv')
