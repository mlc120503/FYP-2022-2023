import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CityU_ee.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.ee.cityu.edu.hk/people/Academic_Staff/Faculty_Staff')
    df = pd.DataFrame(columns=['name', 'PhD'])

    name_e = driver.find_elements(By.XPATH, '//p[@class="people-name"]')
    info_e = driver.find_elements(By.XPATH, '//div[@class="text-top"]')

    for i in range(len(name_e)):
        name = name_e[i].text.split('.')[-1].strip()
        info = info_e[i].find_elements(By.XPATH, './p[3]')
        if name and info:
            info = info[0].text
            t = info.split(',')
            for e in range(len(t)):
                for k in ['Ph.D.', 'PhD']:
                    if k in t[e]:
                        if 'Guan' in name or 'Haolia' in name:
                            phd = t[e + 1].strip()
                            if phd:
                                print(name)
                                print(phd)
                                df.loc[len(df)] = [name, phd]
                                break
                        else:
                            phd = t[e][t[e].find(k) + len(k):].strip()
                            if phd:
                                print(name)
                                print(phd)
                                df.loc[len(df)] = [name, phd]
                                break

    df.loc[len(df)] = ['YUEN, Kelvin S Y', 'University of Sussex']
    df.to_excel('./Data/CityU_ee.xlsx', index=False)
    driver.close()


getinfo()