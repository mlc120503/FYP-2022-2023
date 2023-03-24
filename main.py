import os
import pandas as pd
from dict import name_general
from Universities import HKU_ce, HKU_cs, HKU_eee, HKU_imse, HKU_me, HKUST
from Universities import CityU_cs, CityU_ee, CityU_ace, CityU_adse, CityU_bme, CityU_mne, CityU_mse
from Universities import PolyU_aae, PolyU_bme, PolyU_comp, PolyU_ee, PolyU_eie, PolyU_ise, PolyU_me
from Universities import CUHK_cse, CUHK_ee, CUHK_ie, CUHK_bme, CUHK_mae, CUHK_se

HKUST.getinfo()
HKU_cs.getinfo()
HKU_ce.getinfo()
HKU_eee.getinfo()
HKU_imse.getinfo()
HKU_me.getinfo()
CityU_cs.getinfo()
CityU_bme.getinfo()
CityU_ace.getinfo()
CityU_mse.getinfo()
CityU_adse.getinfo()
CityU_ee.getinfo()
CityU_mne.getinfo()
PolyU_aae.getinfo()
PolyU_eie.getinfo()
PolyU_ee.getinfo()
PolyU_comp.getinfo()
PolyU_me.getinfo()
PolyU_ise.getinfo()
PolyU_bme.getinfo()
CUHK_cse.getinfo()
CUHK_ie.getinfo()
CUHK_ee.getinfo()
CUHK_se.getinfo()
CUHK_bme.getinfo()
CUHK_mae.getinfo()

# create a df to store all result, by reading excel in data file
data = pd.DataFrame(columns=['name', 'grad', 'work'])
data_path = "./data/"
all_file = os.listdir(data_path)
for file in all_file:
    if file.split('.')[-1] == 'xlsx':
        if '_' in file:
            u = file.split('_')[0]
        else:
            u = file.split('.')[0]
        df = pd.read_excel("./data/" + file)
        for i in range(len(df)):
            data.loc[len(data)] = [df.iloc[i, 0], df.iloc[i, -1], u]

# generalize the university name, sort the data and output to excel for ref.
name_general(data)
data = data.sort_values(by=["grad", "work", "name"])
data.to_excel('./Result.xlsx', index=False)

# rename the 'name' column
data.rename(columns={'name': 'count'}, inplace=True)

# combine all low freq uni to 'Low Frequency' and count the occurrences
min_num = 20
m1 = data.groupby('grad').grad.transform('count').lt(min_num)
m2 = data['grad'].ne('EduHK' and 'LingU' and 'HKBU' and 'CityU')
data.loc[m1 & m2, 'grad'] = "Others"
data = (
    data.groupby(["grad", "work"],
                 as_index=False, sort=True)
    ["count"].count()
)
data.to_excel('./flowing.xlsx', index=False)
print(data)


# export the dataframe
def return_df():
    return data
