import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():
    if os.path.isfile("./Data/CityU_bme.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cityu.edu.hk/bme/staff-acad.htm')
    time.sleep(1)
    df = pd.DataFrame(columns=['name', 'PhD'])

    readmore = driver.find_elements(By.XPATH, '//img[@class="rounded w-100"]')

    for i in range(len(readmore)):
        driver.execute_script('arguments[0].click();', readmore[i])
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
        time.sleep(1)
        name = driver.find_elements(By.XPATH, '//p[@class="profile-title"]')
        if name:
            info = name[0].find_element(By.XPATH, 'following-sibling::p[1]')
            name = name[0].text
            name = name[name.find('.') + 1:].strip()
            if info:
                phd = info.text
                if 'PhD(' in phd:
                    phd = phd.split("PhD(")[1].split(")")[0].strip()
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
                elif 'PhD (' in phd:
                    phd = phd.split("PhD (")[1].split(")")[0].strip()
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
                elif 'Ph.D.(' in phd:
                    phd = phd.split("Ph.D.(")[1].split(")")[0].strip()
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
                elif 'Ph.D. (' in phd:
                    phd = phd.split("Ph.D. (")[1].split(")")[0].strip()
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
        driver.back()
        time.sleep(1)
        readmore = driver.find_elements(By.XPATH, '//img[@class="rounded w-100"]')

    df.loc[len(df)] = ['AM Hiu Wai Raymond', 'MIT']
    df.loc[len(df)] = ['LU, Jian', 'UTC']
    df.loc[len(df)] = ['CHEN Ting-Hsuan', 'UCLA']
    df.loc[len(df)] = ['Pakpong CHIRARATTANANON', 'Harvard']
    df.loc[len(df)] = ['TIN Chung', 'MIT']
    df.loc[len(df)] = ['WANG Lidai', 'University of Toronto']
    df.loc[len(df)] = ['ZHANG Jiachen', 'University of Toronto']
    df.loc[len(df)] = ['KHOO Bee Luan', 'National University of Singapore']
    df.to_excel('./Data/CityU_bme.xlsx', index=False)
    driver.close()


getinfo()
