import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CUHK_ie.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.ie.cuhk.edu.hk/people/people.shtml')
    df = pd.DataFrame(columns=['name', 'PhD'])

    pros_e = driver.find_elements(By.XPATH, '//a//span[@class="name_e"]')

    for i in range(len(pros_e)):
        title = driver.find_elements(By.XPATH, '//span[@class="title"]')[i]
        if ("by courtesy" or "Adjunct" or "Emeritus") in title.text:
            break
        else:
            driver.execute_script('arguments[0].click();', pros_e[i])
            time.sleep(1)

        if len(driver.window_handles) == 1:
            name_ = driver.find_elements(By.XPATH, '//div[@class="namebox2"]//h2')
            if name_:
                name_p = name_[0].text
                name = name_p[name_p.find('.') + 1:].strip()
                info = driver.find_elements(By.XPATH, '//div[@class="namebox2"]//p')[0].text
                if 'Ph.' in info:
                    one = info[info.find('Ph.'):]
                    two = one.split('(')[1]
                    phd = two[:two.find(')')]
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
                elif 'PhD' in info:
                    one = info[info.find('PhD'):]
                    two = one.split('(')[1]
                    phd = two[:two.find(')')]
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]

            driver.back()
            time.sleep(2)
            pros_e = driver.find_elements(By.XPATH, '//a//span[@class="name_e"]')

        elif len(driver.window_handles) == 2:
            driver.switch_to.window(driver.window_handles[1])
            name_ = driver.find_elements(By.XPATH, '//div[@class="namebox2"]//h2')
            if name_:
                name_p = name_[0].text
                name = name_p[name_p.find('.') + 1:].strip()
                info = driver.find_elements(By.XPATH, '//div[@class="namebox2"]//p')[0].text
                if 'Ph.' in info:
                    one = info[info.find('Ph.'):]
                    two = one.split('(')[1]
                    phd = two[:two.find(')')]
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
                elif 'PhD' in info:
                    one = info[info.find('PhD'):]
                    two = one.split('(')[1]
                    phd = two[:two.find(')')]
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(2)
            pros_e = driver.find_elements(By.XPATH, '//span[@class="name_e"]')

    df.to_excel('./Data/CUHK_ie.xlsx', index=False)
    driver.close()
