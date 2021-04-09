# -*- coding=utf-8 -*-
# @Time :  15:11
# Author : 陆兮索
# @File : 数据挖掘作业第四周.py
# Software : PyCharm
import pandas as pd
import numpy as np
import sklearn
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df1 = pd.read_csv('/users/DataMiningHW1/Wine Reviews/winemag-data_first150k.csv')
df2 = pd.read_csv('/users/DataMiningHW1/Wine Reviews/winemag-data-130k-v2.csv')
df = pd.concat([df1, df2], keys=['df1', 'df2'], axis=0, ignore_index=True)
#前150k行数据全部缺失'taster_name','taster_twitter_handle','title'列的数据
#concat后无法填补，选择填充'invalid'

print(df.dtypes)
#评分'points' 与价格'price'为数值型，
#缺失值考虑用均值或中位数填补
#查看哪些是数值型数据，并给出五数摘要
print(df.describe())

#画出points,price的盒图
plt.figure()
gs=gridspec.GridSpec(1,2)
mpl.rcParams["font.sans-serif"] = ["FangSong"]
ax0=plt.subplot(gs[0,0])
ax0.boxplot(df['points'])
ax0.set_title("points盒图")
ax0.set_ylabel("points")

ax0=plt.subplot(gs[0,1])
ax0.boxplot(df['price'])
ax0.set_title("price盒图")
ax0.set_ylabel("price")
plt.show()
#查看缺失值，判断各列中是否有缺失值
print(df.isnull().any(axis=0))
#除了 'description' 'points' 'winery'均有缺失值

print(df.isnull().sum(axis=0))
#查看各列缺失值数量
#1. country，province，variety 缺失较少，考虑删去
#2.'price'考虑用平均值填充缺失值
#3. 'designation','taster_name','taster_twitter_handle','title' 考虑统一填充'invalid'
#4. region_1,region_2有时值一致，如两者只有一个缺失考虑用另一个填补
df=df.dropna(subset=['country','province','variety'])
df['price'].replace(np.nan,df['price'].mean(),inplace=True)
df['designation'].replace(np.nan,'invalid',inplace=True)
df['taster_name'].replace(np.nan,'invalid',inplace=True)
df['taster_twitter_handle'].replace(np.nan,'invalid',inplace=True)
df['title'].replace(np.nan,'invalid',inplace=True)

missing_values_index = df[df['region_2'].isin([np.nan]) & ~df['region_1'].isnull()].index
# 定位缺失'region_1'的行的行号index
for idx in missing_values_index:
        df.iloc[idx, 8] = df.iloc[idx, 7]

missing_valuse_index_2 = df[df['region_2'].isin([np.nan]) & df['region_1'].isnull()].index
# 定位'region_1'和'region_2'都为空的行号
for idx in missing_values_index:
        df['region_2'].replace(np.nan, 'invalid', inplace=True)
        df['region_1'].replace(np.nan, 'invalid', inplace=True)
print(df.isnull().sum(axis=0))



