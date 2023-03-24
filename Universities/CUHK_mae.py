import os
import json
import re
import time
import jieba
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/CUHK_mae.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www4.mae.cuhk.edu.hk/people/academic-staff/')
    df = pd.DataFrame(columns=['name', 'describe', 'trans', 'split', 'PhD'])

    all = driver.find_elements(By.XPATH, '//div[@class="desc-box"]/ul/li[2]/a')

    for i in range(len(all)):
        title = driver.find_elements(By.XPATH, '//div[@class="title box-show"]')
        title = title[i].text
        if ("by courtesy" and "Adjunct" and "Emeritus" and "Research") in title:
            continue
        else:
            driver.execute_script('arguments[0].click();', all[i])
            time.sleep(1)
            name = driver.find_elements(By.XPATH, '//div[@class="title main-title"]')
            if name:
                name = name[0].text
                if name != "REN Wei 任偉" and name != "LAU Darwin Tat Ming 劉達銘" and name != "LIAO Wei-Hsin 廖維新":
                    info = driver.find_elements(By.XPATH, '//div[@class="col-12 col-lg-7 pp-details editor-content"]/p')
                    if info:
                        for t in info:
                            text = t.text
                            lst = re.findall(r'Ph.D..*?[.]|PhD.*?[.]|Ph.D.*?[.]|Ph.D..*?degrees.*?[.]', text)
                            for k in lst:
                                if 'degree' in k or 'from' in k or 'University' in k or 'degrees' in k:
                                    print(name)
                                    print(k)
                                    df.loc[len(df)] = [name, k, 'trans', 'split', 'PhD']
                                    break

        driver.back()
        time.sleep(1)
        all = driver.find_elements(By.XPATH, '//div[@class="desc-box"]/ul/li[2]/a')

    driver.close()

    url = 'https://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'

    phds = df['describe']
    for i in range(len(df)):
        sentence = phds[i]
        trans = list()
        data = {'i': sentence,
                'from': 'AUTO',
                'to': 'AUTO',
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_REALTlME'}

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }

        res = requests.post(url, headers=headers, data=data)

        # print(res.text)
        t = json.loads(res.text).get('translateResult')[0][0].get('tgt')
        print(t)
        df.iloc[i, 2] = t
        cut = list(jieba.cut(t))
        df.iloc[i, 3] = str(cut)
        print(cut)
        for e in range(len(cut)):
            if '学院' in cut[e] or '大学' in cut[e]:
                if cut[e] == '大学' or cut[e] == '理工大学' or cut[e] == '理工学院':
                    if cut[e] == '理工大学':
                        df.iloc[i, -1] = ''.join(cut[1:e + 1])
                        print(''.join(cut[1:e + 1]))
                        break
                    elif cut[e] == '理工学院':
                        df.iloc[i, -1] = cut[e - 2] + cut[e - 1] + cut[e]
                        print(cut[e - 2] + cut[e - 1] + cut[e])
                        break
                    elif cut[e - 1] == '农工':
                        df.iloc[i, -1] = cut[e - 2] + cut[e - 1] + cut[e]
                        print(cut[e - 2] + cut[e - 1] + cut[e])
                        break
                    elif cut[e - 1] == '工程':
                        df.iloc[i, -1] = cut[-2] + cut[e]
                        print(cut[-2] + cut[e])
                        break
                    else:
                        df.iloc[i, -1] = cut[e - 1] + cut[e]
                        print(cut[e - 1] + cut[e])
                        break
                elif cut[e] == '国立大学':
                    df.iloc[i, -1] = cut[e - 1] + cut[e]
                    print(cut[e - 1] + cut[e])
                    break
                elif cut[e - 1] == '技术' and cut[e] == '学院':
                    df.iloc[i, -1] = cut[e - 2] + cut[e - 1] + cut[e]
                    print(cut[e - 2] + cut[e - 1] + cut[e])
                    break
                elif cut[e - 1] == '建筑':
                    df.iloc[i, -1] = cut[-2]
                    print(cut[-2])
                    break
                else:
                    df.iloc[i, -1] = cut[e]
                    print(cut[e])
                    break
        res.close()
        time.sleep(5)

    df.loc[len(df)] = ['CHEN Fei 陳翡','','','', 'Nagoya University']
    df.loc[len(df)] = ['SONG Xu 宋旭','','','', 'University of Oxford']
    df.loc[len(df)] = ['TSANG Jasmine Winglam 曾泳琳','','','', 'Imperial College London']
    df.loc[len(df)] = ['LAU Darwin Tat Ming 劉達銘', '', '', '', 'University of Melbourne']
    df.loc[len(df)] = ['LIAO Wei-Hsin 廖維新', '', '', '', 'Pennsylvania State University']
    df.loc[len(df)] = ['REN Wei 任偉', '', '', '', 'Stanford University']

    df.to_excel("./Data/CUHK_mae.xlsx", index=False)
