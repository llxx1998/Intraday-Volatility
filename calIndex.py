import math
import pandas as pd
import numpy as np

df = pd.read_csv('./sp500index.csv')
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
df = df.set_index(keys=['permno', 'date'])

"""
Calculate Intraday Volatility
"""
r1 = np.array(df['askhi'] / df['bidlo'])

r2 = np.array(df['prc'] / df['openprc'])
df['Vohlc'] = np.power(0.5 * np.power(np.log(r1), 2) - (2*math.log(2) - 1) * np.power(np.log(r2), 2), 0.5)
dta1 = df[['Vohlc']]
result = None
"""
Calculate Historical Volatility
"""
dta2 = dta1.copy(deep=True)
df = df[['prc']]
comp_list = df.index.get_level_values('permno').unique().values
back_days = 20
for i in comp_list:
    sub = df.loc[i, :]
    sub = sub.sort_index()
    sub['prc'] = np.log(sub['prc'])
    sub['prc_lag'] = sub['prc'].shift(1)
    sub['log_ret'] = sub['prc'] - sub['prc_lag']
    sub = sub.iloc[1:, :]
    sub['hist_vol'] = None
    sub = sub[['log_ret', 'hist_vol', 'prc']]
    for ix in range(back_days-1, sub.shape[0]):
        # [ix - backdays, ix)
        sub.iloc[ix, 1] = sub.iloc[ix - back_days + 1:ix + 1, 0].std()
    sub = sub.dropna(subset=['hist_vol'])
    sub['date'] = sub.index
    sub['permno'] = i
    sub = sub.set_index(keys=['permno', 'date'])
    sub = sub[['log_ret', 'hist_vol']]
    if result is None:
        result = sub
    else:
        result.append(sub)
dta2 = pd.merge(dta2, result, how='left', left_index=True, right_index=True)
dta2[['Vohlc', 'hist_vol']].to_csv('./sp500_volatility.csv', index=True)

