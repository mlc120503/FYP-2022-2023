import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():
    if os.path.isfile("./Data/PolyU_eie.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.polyu.edu.hk/eie/people/academic-staff/')
    df = pd.DataFrame(columns=['name', 'phd'])

    pros = driver.find_elements(By.XPATH, '//span[@class="ppl-detail-blk__name theme-color-text underline-link__line"]')

    info_e = driver.find_elements(By.XPATH, '//p[@class="ppl-detail-blk__grade"]')
    print(len(pros))
    print(len(info_e))
    j = 0
    for i in range(len(pros)):
        name = ' '.join(pros[i].text.split()[1:])
        if name:
            if 'LIU Ai-Qun' in name or 'LIN Wei' in name:
                continue
            if 'CHEN Menglin' in name:
                break

            info = info_e[j].text
            phd_exist = 'PhD' in info
            if phd_exist:
                one = info[info.find('PhD') + 3:]
                phd = one[one.find('(') + 1: one.find(')')].strip()
                print(name)
                print(phd)
                df.loc[len(df)] = [name, phd]
            j += 1

    df.loc[len(df)] = ["LIN Wei", "City University of Hong Kong"]
    df.loc[len(df)] = ["LIU Ai-Qun", "The National University of Singapore"]
    df.loc[len(df)] = ["CHEUNG Chi-Chung, Lawrence", "HKUST"]
    df.loc[len(df)] = ["LAI Po-Yan, Pauli", "HKU"]
    df.to_excel('./Data/PolyU_eie.xlsx', index=False)
    driver.close()

