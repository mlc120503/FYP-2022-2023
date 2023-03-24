import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CUHK_se.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.se.cuhk.edu.hk/people/academic-staff/')
    df = pd.DataFrame(columns=['name', 'PhD'])

    all = driver.find_elements(By.XPATH, '//td[@class="column-2"]/a')

    for i in range(len(all)):
        driver.execute_script('arguments[0].click();', all[i])
        time.sleep(1)
        title = driver.find_elements(By.XPATH, '//div[@class="wpb_text_column wpb_content_element wpb_animate_when_almost_visible wpb_fadeInDown fadeInDown wpb_start_animation animated"]/div/p[0]')
        if ("by courtesy" and "Adjunct" and "Emeritus" and "Research") in title.text:
            continue
        else:
            name = driver.find_elements(By.XPATH, '//span[@class="breadcrumb_last"]')[0].text
            info = driver.find_elements(By.XPATH, '//div[@class="wpb_text_column wpb_content_element wpb_animate_when_almost_visible wpb_fadeInDown fadeInDown wpb_start_animation animated"]/div/p[0]')
            if info:
                if "PhD (" in info:
                    phd = info.split("PhD (")[1].split(")")[0].strip()

            if phd:
                print(name)
                print(phd)
                df.loc[len(df)] = [name, phd]

        driver.back()
        time.sleep(1)
        all = driver.find_elements(By.XPATH, '//td[@class="column-2"]/a')

    df.to_excel('./Data/CUHK_se.xlsx', index=False)
    driver.close()
