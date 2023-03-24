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

    if os.path.isfile("./Data/CityU_ace.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cityu.edu.hk/ace/about-us/people/academic-staff')
    df = pd.DataFrame(columns=['name', 'describe', 'trans', 'split', 'PhD'])
    time.sleep(2)
    all = driver.find_elements(By.XPATH, '//div[@class="views-field views-field-title"]')

    for i in range(len(all)):
        driver.execute_script('arguments[0].click();', all[i])
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        time.sleep(2)
        name = driver.find_elements(By.XPATH, '//h1[@class="personname"]')
        if name:
            if name[0].text in ("Dr. Kostas SENETAKIS", "Dr. TALAMINI Gianni", "Dr. XUE Qiuli Charlie (薛求理)", "Dr. LU Guoyang (陸國陽)"):
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue
            name = name[0].text
        info = driver.find_elements(By.XPATH, '//div[@class="textblock"]/p/span')
        info2 = driver.find_elements(By.XPATH, '//div[@class="textblock"]/p')
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
        elif info2:
            for t in info2:
                text = t.text
                lst = re.findall(r'Ph.D..*?[.]|PhD.*?[.]|Ph.D.*?[.]|Ph.D..*?degrees.*?[.]', text)
                for k in lst:
                    if 'degree' in k or 'from' in k or 'University' in k or 'degrees' in k:
                        print(name)
                        print(k)
                        df.loc[len(df)] = [name, k, 'trans', 'split', 'PhD']
                        break
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(2)
        all = driver.find_elements(By.XPATH, '//div[@class="views-field views-field-title"]')

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
                    elif cut[e-1] == '工程':
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
                elif cut[e-1] == '技术' and cut[e] == '学院':
                    df.iloc[i, -1] = cut[e-2] + cut[e-1] + cut[e]
                    print(cut[e-2] + cut[e-1] + cut[e])
                    break
                elif cut[e-1] == '建筑':
                    df.iloc[i, -1] = cut[-2]
                    print(cut[-2])
                    break
                else:
                    df.iloc[i, -1] = cut[e]
                    print(cut[e])
                    break
        res.close()
        time.sleep(5)

    df.loc[len(df)] = ['Dr. Kostas SENETAKIS','','','', 'Aristotle University of Thessaloniki']
    df.loc[len(df)] = ['Dr. TALAMINI Gianni','','','', 'Università Iuav di Venezia']
    df.loc[len(df)] = ['Dr. LU Guoyang (陸國陽)','','','', 'RWTH Aachen University']
    df.loc[len(df)] = ['LIEW Kim Meow','','','', 'National University of Singapore']
    df.loc[len(df)] = ['TSOU Jin Yeu','','','', 'UMICH']
    df.loc[len(df)] = ['LI Hin Wa','','','', 'CityU']
    df.loc[len(df)] = ['WANG Yu','','','', 'Cornell']
    df.loc[len(df)] = ['Mei-yung LEUNG','','','', 'HK']
    df.loc[len(df)] = ['Paulina Maria NEISCH','','','', 'Université Paris-Nanterre']

    df.to_excel("./Data/CityU_ace.xlsx", index=False)
