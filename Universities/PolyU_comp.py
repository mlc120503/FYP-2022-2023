import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/PolyU_comp.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.polyu.edu.hk/comp/people/academic-staff/')
    df = pd.DataFrame(columns=['name', 'PhD'])

    pros = driver.find_elements(By.XPATH, '//span[@class="ppl-detail-blk__name theme-color-text underline-link__line"]')

    for i in range(len(pros)):

        driver.execute_script('arguments[0].click();', pros[i])
        time.sleep(2)
        n = driver.find_elements(By.XPATH, '//h2')
        title = driver.find_elements(By.XPATH, '//p[@class="ppl-detail-blk__dept theme-color-text tail-title"]')
        if "Research Assistant" in title[0].text:
            break
        name = n[0].text.split('.')[-1].strip()
        info = driver.find_elements(By.XPATH, '//p[@class="ppl-detail-blk__desc"]')
        if info:
            info_text = info[0].text
            if 'PhD' in info_text:
                phd_ = info_text[info_text.find('PhD') + 4:]
                phd = phd_[:phd_.find(')')].replace(' ', '').replace('(', '')
                print(name)
                print(phd)
                df.loc[len(df)] = [name, phd]
        driver.back()
        time.sleep(3)
        pros = driver.find_elements(By.XPATH, '//span[@class="ppl-detail-blk__name theme-color-text underline-link__line"]')
        time.sleep(2)

    df.to_excel('./Data/PolyU_comp.xlsx', index=False)
    driver.close()