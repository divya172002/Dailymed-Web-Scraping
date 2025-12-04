from selenium import webdriver
from selenium.webdriver.chrome.service import Service#used to configure and launch the Chrome WebDriver service when using Chrome
from selenium.webdriver.common.by import By#locate web elements
from selenium.webdriver.support.ui import WebDriverWait #Helps implement explicit waits,rather than blindly moving ahead in the script, you wait until some condition (like “an element is present” or “clickable”) is met
from selenium.webdriver.support import expected_conditions as EC#A collection of common conditions to use with WebDriverWait, like “element is visible”, “element exists in DOM”, “element is clickable”, etc.
from webdriver_manager.chrome import ChromeDriverManager#This helps you automatically download, install and manage the correct version of chromedriver that matches your browser version
import pandas as pd
import os
import time
import glob#Helps you find (match) multiple files based on patterns (wildcards). For example, if you have many CSV files in a folder and you want to read them all, glob.glob("folder/*.csv") returns a list of matching filenames.
import shutil#higher-level file operations

# PDF download folder

DOWNLOAD_DIR = os.path.join(os.getcwd(), "pdf_downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)

df = pd.read_excel("chemicals.xlsx")

# Function: wait for new PDF + rename it

def wait_and_rename(new_name):
    before = set(glob.glob(os.path.join(DOWNLOAD_DIR, "*.pdf")))

    # Wait for new file to appear
    for _ in range(20):  
        time.sleep(0.5)
        after = set(glob.glob(os.path.join(DOWNLOAD_DIR, "*.pdf")))
        new_files = after - before
        if new_files:
            latest = list(new_files)[0]
            shutil.move(latest, os.path.join(DOWNLOAD_DIR, new_name))
            print(f"✔ Saved PDF as {new_name}")
            return
    



# Main loop

for chem in df["chemical"].iloc[519:]:
    print(f"\n🔍 Searching: {chem}")

    try:
        driver.get("https://dailymed.nlm.nih.gov/dailymed/")

        search_box = wait.until(EC.presence_of_element_located((By.ID, "searchQuery")))
        search_box.clear()
        search_box.send_keys(chem)
        search_box.submit()
        time.sleep(1)

        # ------------------------------------------------
        # CASE 1: Multiple results page
        # ------------------------------------------------
        results = driver.find_elements(By.XPATH, "//a[contains(@href, '/dailymed/drugInfo.cfm')]")

        if len(results) > 0:
            print(f"➡ Found {len(results)} search results")

            for i in range(len(results)):
                # Re-collect to avoid stale elements
                fresh_results = driver.find_elements(By.XPATH, "//a[contains(@href, '/dailymed/drugInfo.cfm')]")

                if i >= len(fresh_results):
                    
                    continue

                print(f"  → Opening result {i+1}")
                fresh_results[i].click()
                time.sleep(1)

                # Try PDF
                try:
                    pdf_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'PDF')]")))
                    pdf_link.click()
                    pass
                    wait_and_rename(f"{chem}_{i+1}.pdf")
                except:
                    pass

                driver.back()
                time.sleep(1)

        else:
            pass

            try:
                pdf_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'PDF')]")))
                pdf_link.click()
                wait_and_rename(f"{chem}_1.pdf")
            except:
                pass

    except Exception as e:
        print(f"{e}")

driver.quit()

