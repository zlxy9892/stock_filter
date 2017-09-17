# -*- coding: utf-8 -*-



### ------------------ 筛选条件 ------------------ ###
# 当前价位高于前一段时间最低价的最大比例
fluct_max = 0.1

# 前一段时间的起始计算时间
date_start = '2017-01-01'

# 年度每股收益最小值
eps_year_min = 0.0

# 收益业绩筛选年份
report_years = [2015, 2016]

# 总股本-亿元
totals_min = 0.7
totals_max = 2.5

# 当前价格
cur_price_min = 1.0
cur_price_max = 30.0

# 市盈率
pe_min = 0.0
pe_max = 200.0

# 上市时间
timeToMarket_min = 20100101
timeToMarket_max = 20170901

# 股东人数
holders_min = 1
holders_max = 100000

# 每股收益
esp_min = -9999.0
esp_max = 9999.0
### ----------------------------------------------------- ###





# 导入依赖库
import tushare as ts
import pandas as pd
import time
import os

print('\n------------- 参数列表 ------------- \n')
print('当前价位高于前一段时间最低价的最大比例: \n %.2f' % (fluct_max))
print('\n前一段时间的起始计算时间: \n', date_start)
print('\n年度每股收益最小值: \n', eps_year_min)
print('\n收益业绩筛选年份: \n', report_years)
print('\n总股本-亿元: \n %.2f - %.2f' % (totals_min, totals_max))
print('\n当前价格: \n %.2f - %.2f' % (cur_price_min, cur_price_max))
print('\n市盈率: \n %.2f - %.2f' % (pe_min, pe_max))
print('\n上市时间起始点: \n', timeToMarket_min)
print('\n股东人数: \n %.2f - %.2f' % (holders_min, holders_max))


print('\n------- 确认以上参数后, 按任意键开始 -------\n')
os.system('pause')

# 导入基本面数据
print('\n### 加载基本面数据...')
df_basic = ts.get_stock_basics()

### --------- 开始筛选 --------- ###
print('\n### 进行基本面筛选...')
#ix = (df_basic.totals > totals_min) & (df_basic.totals < totals_max) & (df_basic.pe > pe_min) & (df_basic.pe < pe_max)
df_res = df_basic[(df_basic.totals >= totals_min) & (df_basic.totals <= totals_max) &
                  (df_basic.pe >= pe_min) & (df_basic.pe <= pe_max) &
                  (df_basic.timeToMarket >= timeToMarket_min) & (df_basic.timeToMarket <= timeToMarket_max) &
                  (df_basic.holders >= holders_min) & (df_basic.holders <= holders_max) &
                  (df_basic.esp >= esp_min) & (df_basic.esp <= esp_max)
                  ]

print('\n### 进行业绩筛选...')
drop_indices = []
reports = []
#rep_2014_4 = ts.get_report_data(2014, 4)  # 同步业绩数据
#rep_2014_4.to_csv('./data/rep_2014_4.csv', encoding='utf-8') # 保存业绩数据
for year in report_years:
    filename = 'data/report_' + str(year) + '_4.csv'
    report_one_year = pd.read_csv(filename, encoding='utf-8', dtype=str)
    reports.append(report_one_year)
for code in df_res.index:
    for report_one_year in reports:
        eps_year = report_one_year[report_one_year.code == code].eps
        if not eps_year.empty:
            eps_year = float(eps_year.values[0])
            if eps_year != 'nan':
                if eps_year < eps_year_min:
                    drop_indices.append(code)
df_res = df_res.drop(drop_indices)

### 筛选当前价位不高于前一段时间的最低价
print('\n### 进行相对低价位筛选...')
date_end = time.strftime('%Y-%m-%d', time.localtime())
drop_indices = []
iter = 0.0
for code in df_res.index:
    iter += 1
    one_stock_hist = ts.get_hist_data(code=code, start=date_start, end=date_end)            
    if len(one_stock_hist) < 30:
        drop_indices.append(code)
        continue
    if one_stock_hist.close[0] > cur_price_max:
        drop_indices.append(code)
        continue
    lowest_price = min(one_stock_hist.low)
    current_price = one_stock_hist.close[0]
    if ((current_price - lowest_price) / lowest_price > fluct_max):    # 当前价位是否较低
        drop_indices.append(code)
    if iter % 10 == 0:
        print('\r正在计算: %5.1f' % (100*float(iter)/len(df_res)), '%', end='')
    
df_res = df_res.drop(drop_indices)

# 导出最终结果
df_res.to_excel('./股票筛选结果.xlsx')

print('\n\n--- 完成! 按任意键退出---\n')
os.system('pause')
