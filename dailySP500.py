import pandas as pd
import wrds

conn = wrds.Connection(wrds_username='xiaolou')
sp500 = conn.raw_sql("""select a.permno, b.date, b.ret, b.prc, b.openprc, b.askhi, b.bidlo, b.vol
                        from crsp.dsp500list as a, crsp.dsf as b
                        where a.permno=b.permno
                        and b.date >= a.start and b.date<= a.ending
                        and b.date>='01/01/1993'
                        order by date;
                        """, date_cols=['start', 'ending', 'date'])
sp500['permno'] = sp500['permno'].astype(int).astype(str)
conn.close()
sp500.to_csv("./dailySP500.csv", index=False)