from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By #By is used for selector
import time
import os

#load excel data
df=pd.read_excel('chemicals.xlsx')
# print(df.columns.tolist())#['chemical']

#set up selenium
driver = webdriver.Chrome()

for chem in df['chemical'].head(10):
    try:
        driver.get(f"https://dailymed.nlm.nih.gov/dailymed/")
        search_box = driver.find_element(By.ID, 'searchQuery')# find the search input and enter the name
        search_box.clear()  #This removes any existing text inside the search box.
        search_box.send_keys(chem) #Types the string stored in chem into the search input box.
        search_box.submit() #Equivalent to pressing Enter manually and page will load for that chemical

        #write logic for getting desired data in html files
        # elems = driver.find_elements(By.CSS_SELECTOR, ".DataElementsTables toggle-content closed long-content scrollingtable")
        

        
        # for elem in elems:
            
        #     d=elem.get_attribute('outerHTML')
        #     print(d.text)
        #     with open(f"data/{chem}_{file}.html","w",encoding="utf-8") as f:
        #         f.write(d)
        #         file+=1
        table_divs = driver.find_elements(
        By.CSS_SELECTOR,
        ".DataElementsTables.toggle-content.closed.long-content.scrollingtable"
        
    )
        
        for idx, elem in enumerate(table_divs, start=1):
            html_string = elem.get_attribute('outerHTML')
            os.makedirs("data", exist_ok=True)
            with open(f"data/{chem}.html", "w", encoding="utf-8") as f:
                f.write(html_string)
                
    except Exception as e:
        print(e)
        pass
    


time.sleep(2)
driver.close()

