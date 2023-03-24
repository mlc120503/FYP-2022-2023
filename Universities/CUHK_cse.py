import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CUHK_cse.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cse.cuhk.edu.hk/people/faculty/')
    df = pd.DataFrame(columns=['name', 'PhD'])

    pros_e = driver.find_elements(By.XPATH, '//div[@class="sptp-icon text-center"]')
    pros_m = driver.find_elements(By.XPATH, '//div[@class="sptp-member-profession"]')
    for pro in range(len(pros_e)):
        if ("Emeritus" or "by courtesy" or "Adjunct") in pros_m[pro].text:
            continue
        driver.execute_script('arguments[0].click();', pros_e[pro])
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        name_ = driver.find_elements(By.XPATH, '//h1')
        if name_:
            name = name_[0].text
            if name in df['name'].values:
                break
            info = driver.find_elements(By.XPATH, '//span[@style="font-size: 14pt;"]')
            if info:
                info = info[0].text
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
        time.sleep(1)

    df.loc[len(df)] = ["FU, Ada Waichee","Simon Fraser University"]
    df.loc[len(df)] = ["Kwong Sak Leung", "Lond."]
    df.loc[len(df)] = ["Dahua Lin", "Massachusetts Institute of Technology"]
    df.loc[len(df)] = ["Sibo WANG", "Nanyang Technological University"]
    df.loc[len(df)] = ["Xiaogang Wang", "Massachusetts Institute of Technology"]
    df.loc[len(df)] = ["WONG, Chak-Kuen", "Columbia University"]
    df.loc[len(df)] = ["XU, Lei", "Tsinghua"]
    df.loc[len(df)] = ["YU, Xu", "University of Tsukuba"]
    df.loc[len(df)] = ["Martin Ding Fat Wong", "University of Illinois at Urbana-Champaign"]

    df.to_excel("./Data/CUHK_cse.xlsx", index=False)
    driver.close()