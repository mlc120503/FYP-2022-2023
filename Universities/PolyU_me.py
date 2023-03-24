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

    if os.path.isfile("./Data/PolyU_me.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.polyu.edu.hk/me/people/academic-teaching-staff/')
    df = pd.DataFrame(columns=['name', 'describe', 'trans', 'split', 'PhD'])

    pros = driver.find_elements(By.XPATH, '//span[@class="ppl-detail-blk__name theme-color-text underline-link__line"]')

    for i in range(len(pros)):
        name = ' '.join(pros[i].text.split()[1:])
        if name == "Abdelrahman Elsayed Elsayed Eltoukhy":
            break
        elif name in ["LEUNG Woon Fong, Wallace 梁煥方 (Prof.)", "LIU Qiang 劉強 (Dr)", "SUN Yuxiang 孫宇翔 (Dr)",
                      "Chenglei 王成磊 (Dr)", "Xiaoliang 於曉亮 (Dr)", "Zengbao 焦增寶 (Dr)", "Hui 唐輝 (Dr)",
                      "Wai On 黃偉安 (Dr)", ""]:
            continue
        driver.execute_script('arguments[0].click();', pros[i])
        time.sleep(3)
        info = driver.find_elements(By.XPATH, '//div[@class="fusion-separator fusion-full-width-sep sep-single sep-solid"]/span')
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

    df.loc[len(df)] = ["CHENG Li 成利 (Prof.)", "", "", "", "Institut National des Sciences Appliquées de Lyon"]
    df.loc[len(df)] = ["CHENG Song 成松 (Dr)", "", "", "", "The University of Melbourne"]
    df.loc[len(df)] = ["CHOY Yat Sze 蔡逸思 (Dr)", "", "", "", "PolyU"]
    df.loc[len(df)] = ["CHU Kar Hang, Henry 朱嘉行 (Dr)", "", "", "", "University of Toronto"]
    df.loc[len(df)] = ["JIAO Zengbao 焦增寶 (Dr)", "", "", "", "CityU"]
    df.loc[len(df)] = ["LIU Yang 劉陽 (Dr)", "", "", "", "The University of Sydney"]
    df.loc[len(df)] = ["David NAVARRO-ALARCON 毛大衛 (Dr)", "", "", "", "CUHK"]
    df.loc[len(df)] = ["SU Zhongqing 蘇眾慶 (Prof.)", "", "", "", "The University of Sydney"]
    df.loc[len(df)] = ["WANG Liqiu 王立秋 (Prof.)", "", "", "", "University of Alberta"]
    df.loc[len(df)] = ["WANG Zuankai 王鑽開 (Prof.)", "", "", "", "Rensselaer Polytechnic Institute"]
    df.loc[len(df)] = ["WONG Wai On 黃偉安 (Dr)", "", "", "", "PolyU"]
    df.loc[len(df)] = ["YAO Haimin 姚海民 (Dr)", "", "", "", "Universität Stuttgart"]
    df.loc[len(df)] = ["YU Xiang 余翔 (Dr)", "", "", "", "PolyU"]
    df.loc[len(df)] = ["ZHENG Guangping 鄭廣平 (Dr)", "", "", "", "Johns Hopkins University"]
    df.loc[len(df)] = ["TANG Hui 唐輝 (Dr)", "", "", "", "Manchester"]
    df.to_excel('./Data/PolyU_me.xlsx', index=False)


getinfo()