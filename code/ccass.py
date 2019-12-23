from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd
import os
import time
from datetime import datetime


class ccass:
    
    def __init__(self):

        import datetime
        date = datetime.datetime.now()+ datetime.timedelta(hours=8)
        self.date = str(date.date())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
        print('successfully launch driver')

    def get_table(self, n):
        self.driver.get('https://www.hkexnews.hk/sdw/search/searchsdw.aspx')
        txtStockCode = self.driver.find_element_by_name('txtStockCode')
        txtStockCode.send_keys(n)
        btnSearch = self.driver.find_element_by_id('btnSearch')
        btnSearch.click()

        source = self.driver.page_source
        soup = bs(source)
        table = soup.find('table')
        all_tables = table.find_all('tr')[1:]
        df = pd.DataFrame([[i.text.replace('\n','') for i in t.find_all('td')] for t in all_tables])
        df.columns = ['id','name','address','shareholding','number']

        name_replace = 'Name of CCASS Participant (* for Consenting Investor Participants ):'
        number_replace = "% of the total number of Issued Shares/ Warrants/ Units:"

        df['name'] = df.name.apply(lambda x: x.replace(name_replace,''))
        df['address'] = df.address.apply(lambda x: x.replace('Address:',''))
        df['shareholding'] = df.shareholding.apply(lambda x: x.replace('Shareholding:',''))
        df['number'] = df.number.apply(lambda x: x.replace(number_replace,''))
        df.columns = ['ccass_id','name','address','holding','stake']
        df['stake'] = df.stake.apply(lambda x: float(x.replace('%','')))
        df['holding'] = df.holding.apply(lambda x: int(x.replace(',','')))
        df['cumul_stake'] = df.stake.cumsum()
        df['lastchange'] = ''
        df['file_date'] = self.date
        df['taker'] = n
        df['row'] = range(len(df))
        df['row'] = df['row'].astype(float)
        df['ccass_id'] = df['ccass_id'].apply(lambda x: x.replace('Participant ID:',''))
        df = df[['row','ccass_id','name','holding','lastchange','stake','cumul_stake','file_date','taker']]

        return df