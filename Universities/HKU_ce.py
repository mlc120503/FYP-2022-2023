import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/HKU_ce.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.civil.hku.hk/h2_acstaff.html')
    time.sleep(1)
    df = pd.DataFrame(columns=['name', 'PhD'])

    all = driver.find_elements(By.XPATH,'//h4/a')
    pros = driver.find_elements(By.XPATH,'//h4/a/strong')

    for i in range(len(all)):
        if pros[i]:
            name = pros[i].text
        driver.execute_script('arguments[0].click();', all[i])
        time.sleep(1)
        info = driver.find_elements(By.XPATH, '//strong')[0]
        if info:
            info = info.text
            match = re.search(r'PhD, (.+)', info)
            match2 = re.search(r'Ph.D., (.+)', info)
            match3 = re.search(r'PhD (.+)', info)
            if match:
                phd = match.group(1)
                driver.back()
            elif match2:
                phd = match2.group(1)
                driver.back()
            elif match3:
                phd = match3.group(1)
                driver.back()
            else:
                driver.back()
                continue
            phd = phd.split(",")[0].strip()
            print(name)
            print(phd)
            df.loc[len(df)] = [name, phd]

        all = driver.find_elements(By.XPATH, '//h4/a')
        pros = driver.find_elements(By.XPATH, '//h4/a/strong')
        time.sleep(1)

    df.to_excel("./Data/HKU_ce.xlsx", index=False)
    driver.close()
