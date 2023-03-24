import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():
    if os.path.isfile("./Data/CityU_mne.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cityu.edu.hk/mne/people/academic-staff')
    df = pd.DataFrame(columns=['name', 'PhD'])

    more = driver.find_elements(By.XPATH, '//div[@class="col-md-6 mb-3"]/h5/a')

    for i in range(len(more)):

        name = more[i].text
        name = name[name.find('.') + 1:].strip()
        if name == "ZHU, Yuntian":
            df.loc[len(df)] = ['PAN, Chin', 'National Tsing Hua University']
            df.loc[len(df)] = ['KUO, Way', 'Kansas State University']
            df.loc[len(df)] = ['LIU Chain Tsuan', 'Brown University']
            df.loc[len(df)] = ['HIBIKI, Takashi', 'Osaka University']
            df.loc[len(df)] = ['LEE Duu-Jong', 'National Taiwan University']
            df.loc[len(df)] = ['LU, Jian', 'UTC']
            df.loc[len(df)] = ['KAI, Ji-Jung', 'University of Wisconsin-Madison']
            df.loc[len(df)] = ['YANG Yong', 'Princeton University']
            df.loc[len(df)] = ['JING, Xingjian', 'Chinese Academy of Sciences']
            df.loc[len(df)] = ['ZHAO Jiyun', 'Massachusetts Institute of Technology']
            df.loc[len(df)] = ['HU, Alice, Jian', 'Purdue University']
            df.loc[len(df)] = ['YANG, Zhengbao', 'University of Toronto']
            df.loc[len(df)] = ['LI, Weihong', 'Tsinghua University']
            df.loc[len(df)] = ['Steven WANG', 'Monash']
            df.loc[len(df)] = ['DUAN, Penghao', 'University of Oxford']
            df.loc[len(df)] = ['FAN Cuncai', 'Purdue University']
            df.loc[len(df)] = ['ZHAO, Shijun', 'Peking University']
            df.loc[len(df)] = ['LIU, Jun', 'University of Toronto']
            df.to_excel('../../data/CityU/CityU_mne.xlsx', index=False)
            driver.close()
            return
        driver.execute_script('arguments[0].click();', more[i])
        time.sleep(1)

        info = driver.find_elements(By.XPATH, "//div[@class='clearfix text-formatted field field--name-field-degree field--type-text-long field--label-hidden field__item']/p")
        if info:
            phd = info[0].text
            if "PhD(" in phd:
                phd = phd.split("PhD(")[1].split(")")[0].strip()
            elif "PhD (" in phd:
                phd = phd.split('PhD (')[1].split(")")[0].strip()
            elif "Ph.D. (" in phd:
                phd = phd.split('Ph.D. (')[1].split(")")[0].strip()

            if name != "HIBIKI, Takashi" and name != "DUAN, Penghao" and name != "ZHAO, Shijun":
                print(name)
                print(phd)
                df.loc[len(df)] = [name, phd]

        handle = driver.window_handles
        if len(handle) > 1:
            driver.switch_to.window(handle[1])
            driver.close()
            driver.switch_to.window(handle[0])
        else:
            driver.back()

        time.sleep(1)
        more = driver.find_elements(By.XPATH, '//div[@class="col-md-6 mb-3"]/h5/a')

    df.to_excel('./Data/CityU_mne.xlsx', index=False)
    driver.close()

