import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CityU_mse.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cityu.edu.hk/mse/faculty#joint-faculty')
    time.sleep(2)
    df = pd.DataFrame(columns=['name', 'PhD'])

    readmore = driver.find_elements(By.XPATH, '//div[@class="col-md-6 mb-3"]/h5/a')

    for i in range(len(readmore)):
        driver.execute_script('arguments[0].click();', readmore[i])
        time.sleep(2)
        name = driver.find_elements(By.XPATH, '//h1')
        if name:
            name = name[0].text
            name = name[name.find('.') + 1:].strip()
            if name == "CHENG, Shuk Han (鄭淑嫻)":
                break
        # info = driver.find_elements(By.XPATH, '//div[@class="col-md-9 hide-in-mobile"]//p')
        info = driver.find_elements(By.XPATH, '//div[@class="row col-sm-12"]//p')
        if info and name:
            phd = info[0].text
            if 'PhD ' in phd:
                phd = phd.split("PhD ")[1].split(",")[0].strip()
                if '\n' in phd:
                    phd = phd.split('\n')[0].strip()
            elif 'Ph. D., ' in phd:
                phd = phd.split("Ph. D., ")[1].split(",")[0].strip()
            elif 'Ph.D., ' in phd:
                phd = phd.split("Ph.D., ")[1].split(",")[0].strip()
            elif 'Ph.D ' in phd:
                phd = phd.split("Ph.D ")[1].split(",")[0].strip()
        if phd != '':
            print(name)
            print(phd)
            df.loc[len(df)] = [name, phd]
        driver.back()
        time.sleep(2)
        readmore = driver.find_elements(By.XPATH, '//div[@class="col-md-6 mb-3"]//a')

    df.loc[len(df)] = ['Guo HONG', 'Peking University']

    df.to_excel('./Data/CityU_mse.xlsx', index=False)
    driver.close()
