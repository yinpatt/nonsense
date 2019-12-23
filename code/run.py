import scrap
import pandas as pd
c = scrap.ccass()

all_tables = []
for i in l:
  try:
    all_tables.append(c.get_table(i))
  except:
    ''
