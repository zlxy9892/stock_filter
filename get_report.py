import pandas as pd
import tushare as ts


rep_year = 2017
rep_quarter = 4
rep = ts.get_report_data(rep_year, rep_quarter)
rep.to_csv('./data/report_'+str(rep_year)+'_'+str(rep_quarter)+'.csv', encoding='utf-8')

print('--- Done! ---')
