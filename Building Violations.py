# -*- coding=utf-8 -*-
# @Time :  3:24
# Author : 陆兮索
# @File : Building Violations.py
# Software : PyCharm

import pandas as pd
import numpy as np
import sklearn
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_csv('/users/DataMiningHW1/Chicago Building Violations/building-violations.csv')
print(df.dtypes)
#查看哪些是数值型数据，并给出五数摘要
print(df.describe())
#查看缺失值，判断各列中是否有缺失值
print(df.isnull().any(axis=0))
#查看'VIOLATION CODE'的分布
plt.hist(df['VIOLATION CODE'])
plt.title('VIOLATION CODE')
plt.show()
#查看各列缺失值数量
#180万行数据中，'VIOLATION STATUS DATE', 'VIOLATION LOCATION'
#'SSA'缺失都在百万级
#
#'VIOLATION INSPECTOR COMMENTS' 'VIOLATIONDESCRIPTION'
#'VIOLATION ORDIANCE'无法填补 考虑删去所在行
#
#查看violation date和violation status date的关系
#选择用violation date来插补violation status date，即当天解决
print(df[df['VIOLATION STATUS DATE'].isin([np.nan])])
#查看violation date和violation status date的关系
#选择用violation date来插补violation status date，即当天解决
violation_status_date_missing_values_index = df[df['VIOLATION STATUS DATE'].isin([np.nan])].index
#print(violation_status_date_missing_values_index[:500])
for idx in violation_status_date_missing_values_index:
    df.iloc[idx, 5] = df.iloc[idx, 2]



#查看violation description为空值的行，
#发现其violation location也多为空值，
#且为空值的行少于1%，考虑删除为空值的行
df=df.dropna(subset=['VIOLATION DESCRIPTION','VIOLATION ORDINANCE'])
#选择用众数"OTHER   :    :OTHER"填充
df['VIOLATION LOCATION'].replace(np.nan,'OTHER   :    :OTHER',inplace=True)

#VIOLATION INSPECTOR COMMENTS
df['VIOLATION INSPECTOR COMMENTS'].replace(np.nan,'invalid',inplace=True)

#SSA
#用0填充
df['SSA'].replace(np.nan,0,inplace=True)
df['STREET TYPE'].replace(np.nan,'invalid',inplace=True)


#LATITUDE缺失1000多行，考虑删去
df=df.dropna(subset=['LATITUDE','LONGITUDE','LOCATION',
                    'Community Areas','Zip Codes',
                    'Boundaries - ZIP Codes','Census Tracts',
                    'Wards','Historical Wards 2003-2015'])

print(df.isnull().sum(axis=0))



