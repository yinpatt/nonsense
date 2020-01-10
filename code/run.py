import scrap
import pandas as pd
import datetime
from google.cloud import storage
from io import StringIO
import os
import util
import json


#Reading config file
with open('/home/yinpatt/nonsense/code/config.json') as json_file:
    config = json.load(json_file)

#defining google bucket, today, stock code, and load the ccass scraper
gcs = storage.Client('/home/yinpatt/nonsense/code/secret.json')
today = str(datetime.datetime.now()+datetime.timedelta(hours = 8)).split(' ')[0]
all_stock_code = list(pd.read_csv('https://storage.googleapis.com/hedgefund/Mainboard%20List.csv').TICKER)
c = scrap.ccass()

#loop through all tables and get the table
all_tables = []
for i in all_stock_code:
  try:
    print(i)
    all_tables.append(c.get_table(i))
  except:
    ''
df = pd.concat(all_tables)

# Save the table to the related bucket
f = StringIO()
df.to_csv(f)
f.seek(0)
gcs.get_bucket('ccass_raw').blob('daily/main_df/main_df_'+str(today)+'.csv').upload_from_file(f, content_type='text/csv')
c.driver.quit()

#define the date of today and yesterday
td = datetime.datetime.now()+ datetime.timedelta(hours=8)
td = str(td.date())
ytd = datetime.datetime.now()+ datetime.timedelta(hours=8)- datetime.timedelta(hours=24)
ytd = str(ytd.date())


os.chdir(config['main_df_path'] )
df = util.get_table(ytd, td) 
os.chdir(config['excel_path'] )
util.write_xlsx(td, df) 
util.send_email(td, config['email_sender'], config['email_receiver'], config['email_pw'])
