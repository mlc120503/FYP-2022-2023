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

    if os.path.isfile("./Data/PolyU_ise.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.polyu.edu.hk/ise/people/academic-staff/')
    df = pd.DataFrame(columns=['name', 'describe', 'trans', 'split', 'PhD'])

    pros = driver.find_elements(By.XPATH, '//span[@class="ppl-detail-blk__name theme-color-text underline-link__line"]')

    for i in range(len(pros)):
        name = ' '.join(pros[i].text.split()[1:])
        if name == "Abdelrahman Elsayed Elsayed Eltoukhy":
            break
        elif name in ["Prof. Keith K.C. Chan 陳鏡昌", "L.C. Chan 陳聯洲", "Xiaowen Fu 符嘯文","Kun Wang 王焜",
                      "Lidong Yang (楊立冬)", "Xiaoge Zhang 張曉革", "Prof. H.C. Man 文効忠"]:
            continue
        driver.execute_script('arguments[0].click();', pros[i])
        time.sleep(3)
        info = driver.find_elements(By.XPATH, '//div[@class="content"]')
        if info:
            describe = list(re.findall('Ph.D..*?[.]|PhD.*?[.]|graduated.*?[.]', info[0].text))
            if describe:
                print(name)
                print(describe[0])
                df.loc[len(df)] = [name, describe[0], 'trans', 'split', 'PhD']
        driver.back()
        time.sleep(3)
        pros = driver.find_elements(By.XPATH, '//span[@class="ppl-detail-blk__name theme-color-text underline-link__line"]')
        time.sleep(2)

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
                if cut[e] == '大学' or cut[e] == '理工学院' or cut[e] == '理工大学':
                    if cut[e] == '理工学院':
                        if '隶属' in cut[e + 1]:
                            df.iloc[i, -1] = cut[e + 2] + cut[e]
                            print(cut[e + 2] + cut[e])
                            break
                        elif cut[e - 1] == '综合':
                            df.iloc[i, -1] = cut[e - 4] + cut[e - 1] + cut[e]
                            print(cut[e - 4] + cut[e - 1] + cut[e])
                            break
                        else:
                            df.iloc[i, -1] = cut[e - 1] + cut[e]
                            print(cut[e - 1] + cut[e])
                            break
                    elif cut[e - 1] in ['城市', '女王', '纳什']:
                        df.iloc[i, -1] = cut[e - 2] + cut[e - 1] + cut[e]
                        print(cut[e - 2] + cut[e - 1] + cut[e])
                        break
                    elif cut[e - 1] == '克莱德':
                        df.iloc[i, -1] = ''.join(cut[:cut.index(cut[e]) + 1])
                        print(''.join(cut[:cut.index(cut[e]) + 1]))
                        break
                    elif cut[e - 1] == '博士学位':
                        df.iloc[i, -1] = cut[e + 1] + cut[e]
                        print(cut[e + 1] + cut[e])
                        break
                    else:
                        df.iloc[i, -1] = cut[e - 1] + cut[e]
                        print(cut[e - 1] + cut[e])
                        break
                else:
                    df.iloc[i, -1] = cut[e]
                    print(cut[e])
                    break
        res.close()
        time.sleep(5)

    df.loc[len(df)] = ["Keith K.C. Chan 陳鏡昌", "", "", "", "PolyU"]
    df.loc[len(df)] = ["L.C. Chan 陳聯洲", "", "", "", "PolyU"]
    df.loc[len(df)] = ["Xiaowen Fu 符嘯文", "", "", "", "The University of British Columbia"]
    df.loc[len(df)] = ["Prof. Y.M. Li 李楊民", "", "", "", "Tianjin University"]
    df.loc[len(df)] = ["Kun Wang 王焜", "", "", "", "The University of British Columbia"]
    df.loc[len(df)] = ["Lidong Yang (楊立冬)", "", "", "", "CUHK"]
    df.loc[len(df)] = ["Xiaoge Zhang 張曉革", "", "", "", "Vanderbilt University"]
    df.loc[len(df)] = ["H.C. Man 文効忠", "", "", "", "Lond."]
    df.loc[len(df)] = ["Prof. Winco KC Yung容錦泉", "", "", "", "Brunel University London"]
    df.to_excel('./Data/PolyU_ise.xlsx', index=False)
