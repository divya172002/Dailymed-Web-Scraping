from selenium import webdriver
import pandas as pd
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By #By is used for selector
import time
from bs4 import BeautifulSoup

#load excel data
df=pd.read_excel('chemicals.xlsx')
print(df.columns.tolist())

#set up selenium
driver = webdriver.Chrome()

for chem in df['chemical'].head(5):
    try:
        driver.get(f"https://dailymed.nlm.nih.gov/dailymed/")
        # find the search input and enter the name
        search_box = driver.find_element(By.ID, 'searchQuery')  # depends on site
        search_box.clear()
        search_box.send_keys(chem)
        search_box.submit()

        #write logic for getting desired data in html files
        elems = driver.find_element(By.CLASS_NAME, "DataElementsTables")
        # print(elems.text) #gives textual information in cmd itself

        # print(elems.get_attribute('outerHTML'))#it will give you html of that product part

        

        for elem in elems:
            # print(elem.text)
            d=elem.get_attribute('outerHTML')
            with open(f"data/{chem}_{file}.html","w",encoding="utf-8") as f:
                f.write(d)
                file+=1
    except Exception as e:
        print(e)
        pass
    


time.sleep(2)
# driver.close()

