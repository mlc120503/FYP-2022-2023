import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CUHK_ee.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('http://www.ee.cuhk.edu.hk/en-gb/people/academic-staff')
    df = pd.DataFrame(columns=['name', 'PhD'])
    all = driver.find_elements(By.XPATH, '//div[@class="read-more"]/a')

    for e in range(len(all)):
        driver.execute_script('arguments[0].click();', all[e])
        time.sleep(1)
        name = driver.find_elements(By.XPATH, '//div[@class="page-header"]/h1')[0].text[5:]
        sub = driver.find_elements(By.XPATH, '//sub')
        title = driver.find_elements(By.XPATH, '//td[@colspan="3"]')[0]
        if title:
            if ("Emeritus" or "by courtesy") in title.text:
                break
        if sub:
            sub = sub[0].text
            if 'Ph.' in sub:
                one = sub[sub.find('Ph.'):]
                if '(' in one:
                    if 'D.Sc' in one:
                        two = one.split('(')
                        phd = two[2][:two[2].find(')')].strip()
                    else:
                        two = one.split('(')
                        phd = two[1][:two[1].find(')')].strip()
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
            elif 'PhD' in sub:
                one = sub[sub.find('PhD'):]
                if '(' in one:
                    two = one.split('(')
                    phd = two[1][:two[1].find(')')].strip()
                    print(name)
                    print(phd)
                    df.loc[len(df)] = [name, phd]
        driver.back()
        time.sleep(1)
        all = driver.find_elements(By.XPATH, '//div[@class="read-more"]/a')

    #df.drop(df.tail(3).index, inplace=True)

    df.loc[len(df)] = ['Prof BLU, Thierry', 'Telecom Paris']
    df.loc[len(df)] = ['Prof LONG, Yi', 'Cambridge']
    df.loc[len(df)] = ['Prof REN, Hongliang', 'CUHK']
    df.loc[len(df)] = ['Prof XU, Jianbin', 'Universität Konstanz']

    df.to_excel('./Data/CUHK_ee.xlsx', index=False)
    driver.close()
