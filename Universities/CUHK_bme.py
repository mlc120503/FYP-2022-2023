import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

def getinfo():

    if os.path.isfile("./Data/CUHK_bme.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('http://www.bme.cuhk.edu.hk/new/core-faculty.php')
    time.sleep(1)
    df = pd.DataFrame(columns=['name', 'PhD'])

    readmore = driver.find_elements(By.XPATH, '//a[@class="faculty-entry"]')

    for i in range(len(readmore)):
        name = driver.find_elements(By.XPATH, '//div[@class="faculty-name"]')
        if name:
            name = name[i].text
        driver.execute_script('arguments[0].click();', readmore[i])
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(1)
        info2 = driver.find_elements(By.XPATH, '//div[@class="content-text-inner"]')
        if info2:
            info = info2[2]
            info_text = info.text.replace('\n', '').replace('\r', '')
            phd_idx=info_text.find('Ph.D. ')
            if phd_idx !=-1:
                after_phd_text = info_text[phd_idx + 5:]
                if ',' in after_phd_text:
                    phd = after_phd_text.split(',')[1].strip()
                    digit = re.search(r'(.+?)\d+', phd)
                    if digit:
                        phd = digit.group(1)
                        print(name)
                        print(phd)
                        df.loc[len(df)] = [name, phd]
                    else:
                        print(name)
                        print(phd)
                        df.loc[len(df)] = [name, phd]

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        readmore = driver.find_elements(By.XPATH, '//a[@class="faculty-entry"]')

    df.loc[len(df)] = ['Prof. CHOI Chung Hang Jonathan', 'University of Strathclyde']
    df.loc[len(df)] = ['Prof. BEYER, Sebastian', 'National University of Singapore']
    df.loc[len(df)] = ['Prof. DINH Ngoc Duy', 'National University of Singapore']
    df.loc[len(df)] = ['Prof. GAO Zhaoli', 'HKUST']
    df.loc[len(df)] = ['Prof. HO, Ho Pui Aaron', 'University of Nottingham']
    df.loc[len(df)] = ['Prof. MAK, Fuk-tat, Arthur', 'Northwestern University']
    df.loc[len(df)] = ['Prof. YUAN, Wu, Scott', 'CUHK']
    df.loc[len(df)] = ['AU Kwok Wai Samuel', 'MIT']
    df.loc[len(df)] = ['Prof CHAN Hon Fai Vivas', 'Duke University']
    df.loc[len(df)] = ['Prof. CHAN, Michael Kenneth', 'University of California, Berkeley']
    df.loc[len(df)] = ['Prof. CHEN, Weitian', 'University of Virginia']
    df.loc[len(df)] = ['Prof. CHEUNG, W.H. Louis', 'CUHK']
    df.loc[len(df)] = ['Prof. HENG, Pheng Ann', 'Indiana University']
    df.loc[len(df)] = ['Dr. KO, Ho Owen', 'UCL']
    df.loc[len(df)] = ['Professor LI Gang', 'Oxon']
    df.loc[len(df)] = ['Prof. LI, Zheng', 'CUHK']
    df.loc[len(df)] = ['Prof. NG, Wai-Lung Billy', 'CUHK']
    df.loc[len(df)] = ['Professor QIN Ling', 'University of Cologne']
    df.loc[len(df)] = ['Prof. TUAN, Rocky', 'Rockefeller University']
    df.loc[len(df)] = ['Prof WAN Chao', 'Shanghai Jiao Tong University']
    df.loc[len(df)] = ['Prof. Yixiang WANG', 'Shanghai Medical University']
    df.loc[len(df)] = ['Prof YUNG Wing Ho', 'University of Oxford']

    df.to_excel('./Data/CUHK_bme.xlsx', index=False)
    driver.close()


