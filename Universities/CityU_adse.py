import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CityU_adse.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cityu.edu.hk/adse/stafflist.htm')
    time.sleep(1)
    df = pd.DataFrame(columns=['name', 'PhD'])

    tr_elements = driver.find_elements(By.XPATH,'//table[@class="table table-bordered table-striped"]/tbody/tr')
    for tr in tr_elements:
        a = tr.find_elements(By.XPATH, './td[2]/a')
        name = a[0].text
        if "Professor" in name:
            name = name.split("Professor ")[1].strip()
        elif "Dr." in name:
            name = name[name.find('.') + 1:].strip()

        driver.execute_script('arguments[0].click();', a)
        time.sleep(2)

        info = driver.find_elements(By.XPATH, '//div[@class="cityu-content content-color-default"]//p')
        if info:
            phd = info[0].text
            if 'PhD' in phd:
                start = phd.find('(') + 1
                end = phd.find(')', start)
                if 0 < start < end:
                    phd = phd[start:end]
            print(name)
            print(phd)
            df.loc[len(df)] = [name, phd]

        driver.back()
        time.sleep(2)

    df.to_excel("./Data/CityU_adse.xlsx", index=False)
    driver.close()
