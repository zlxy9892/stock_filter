import pandas as pd
import tushare as ts

rep_2014_4 = ts.get_report_data(2014, 4)  # 同步业绩数据
rep_2014_4.to_csv('./data/rep_2014_4.csv', encoding='utf-8') # 保存业绩数据