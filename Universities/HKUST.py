import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


def getinfo():

    if os.path.isfile("./Data/HKUST.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://seng.hkust.edu.hk/about/our-People/faculty')
    df = pd.DataFrame(columns=['name', 'PhD'])

    for i in range(13):
        time.sleep(2)
        pros = driver.find_elements(By.XPATH, '//div[@class="fullname"]')
        for j in range(len(pros)):
            driver.execute_script('arguments[0].click();', pros[j])
            time.sleep(2)
            title = driver.find_elements(By.XPATH, '//div[@class="webtitle-item"]')
            l = 0
            target = True
            for k in title:
                if "Emeritus" in title[l].text or "Adjunct" in title[l].text or "Research" in title[l].text or "Visiting" in title[l].text:
                    target = False
                    break
                l = l+1
            if target:
                phd = driver.find_elements(By.XPATH,
                                           '//div[@class="field field--name-field-degree field--type-string field--label-visually_hidden"]//div[@class="field__item"]')
                if phd:
                    PhDs = phd[0].text
                    PhD = PhDs[PhDs.find(',') + 2:]
                    fn = driver.find_elements(By.CLASS_NAME, 'first-name')
                    ln = driver.find_elements(By.CLASS_NAME, 'last-name')
                    cn = driver.find_elements(By.CLASS_NAME, 'chinese-name')
                    if cn:
                        name = [fn[0].text, ln[0].text, cn[0].text]
                    else:
                        name = [fn[0].text, ln[0].text]
                    df.loc[len(df)] = [' '.join(name), PhD]
                    print(f'{" ".join(name)}:{PhD}')
                else:
                    print('NULL')

                driver.back()
                time.sleep(2)
            else:
                driver.back()
                time.sleep(2)

        page = driver.find_elements(By.XPATH, '//a[@aria-label="next page"]')[0]
        driver.execute_script('arguments[0].click();', page)

    df.to_excel('./Data/HKUST.xlsx', index=False)
    driver.close()
