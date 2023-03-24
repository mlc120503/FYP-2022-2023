import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CityU_cs.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cs.cityu.edu.hk/people/academic-staff')
    df = pd.DataFrame(columns=['name', 'PhD'])

    name_e = driver.find_elements(By.XPATH, '//div[@class="name"]')
    info_e = driver.find_elements(By.XPATH, '//div[@class="study"]')
    for i in range(len(name_e)):
        name = ' '.join(name_e[i].text.split()[1:])
        info = info_e[i].text
        phd = []
        for e in info.split(','):
            for k in ['Ph.D.', 'PhD', 'DSc']:
                if k in e:
                    if 'DSc' in e:
                        phd.append(e[e.find(k) + len(k) + 1:].strip())
                    elif '(' in e:
                        temp = e[e.find(k):]
                        phd.append(temp[temp.find('(') + 1:temp.find(')')])
                    else:
                        phd.append(e[e.find(k) + len(k) + 1:].strip())
        if phd:
            print(name)
            print(','.join(phd))
            df.loc[len(df)] = [name, ','.join(phd)]

    df.to_excel('./Data/CityU_cs.xlsx', index=False)
    driver.close()
