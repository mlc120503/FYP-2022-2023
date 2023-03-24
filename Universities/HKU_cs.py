import os
import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By


def getinfo():

    if os.path.isfile("./Data/HKU_cs.xlsx"):
        return None

    driver = webdriver.Chrome()
    driver.get('https://www.cs.hku.hk/people/academic-staff')

    # find pros name,only name can click
    pro_lst = driver.find_elements(By.XPATH, '//div[@class="left col-8 col-sm-8"]//strong')
    df = pd.DataFrame(columns=['name', 'PhD'])
    name = pro_lst[0].text
    driver.execute_script('arguments[0].click();', pro_lst[0])
    sed = driver.find_elements(By.XPATH, '//strong//em')
    if sed:
        if len(sed) >= 2:
            df.loc[len(df)] = [name, sed[1].text]
            print(f'{name} : {sed[1].text}')
        else:
            df.loc[len(df)] = [name, sed[0].text]
            print(f'{name} : {sed[0].text}')
    else:
        ot = driver.find_elements(By.XPATH, '//strong')
        df.loc[len(df)] = [name, ot[0].text]
        print(f'{name} : {ot[0].text}')
    time.sleep(1)
    driver.back()
    for i in range(1, len(pro_lst)):
        pro_lst = driver.find_elements(By.XPATH, '//div[@class="left col-8 col-sm-8"]//strong')
        time.sleep(1)  # in order to wait name loaded,can decrease
        name = pro_lst[i].text
        driver.execute_script('arguments[0].click();', pro_lst[i])
        time.sleep(1)
        sed = driver.find_elements(By.XPATH, '//strong//em')
        if sed:
            if len(sed) >= 3:
                if name == 'Chin, Francis Y.L.':
                    print(f'{name} : {sed[1].text.strip().replace("Assistant Professor", "")}')
                    df.loc[len(df)] = [name, sed[1].text.strip().replace("Assistant Professor", "")]
                else:
                    print(f'{name} : {sed[2].text.strip().replace("Assistant Professor", "")}')
                    df.loc[len(df)] = [name, sed[2].text.strip().replace("Assistant Professor", "")]
            elif len(sed) == 2:
                print(f'{name} : {sed[1].text.strip().replace("Assistant Professor", "")}')
                df.loc[len(df)] = [name, sed[1].text.strip().replace("Assistant Professor", "")]
            else:
                df.loc[len(df)] = [name, sed[0].text.strip().replace("Assistant Professor", "")]
                print(f'{name} : {sed[0].text.strip().replace("Assistant Professor", "")}')
        else:
            ot = driver.find_elements(By.XPATH, '//strong')
            if ot:
                if name == 'Kong, Lingpeng':
                    df.loc[len(df)] = [name, ot[0].text.strip("PhD").strip().replace("Assistant Professor", "")]
                    print(f'{name} : {ot[0].text.strip("PhD").strip().replace("Assistant Professor", "")}')
                elif name == 'Lam, Edmund Y. M.' or name == "Liu, Xihui" or name == "Luo, Hao":
                    driver.back()
                    continue
                else:
                    df.loc[len(df)] = [name, ot[0].text.strip().replace("Assistant Professor", "")]
                    print(f'{name} : {ot[0].text.strip().replace("Assistant Professor", "")}')
            else:
                driver.back()
                continue

        driver.back()

    df.to_excel('./Data/HKU_cs.xlsx', index=False)
    driver.close()

