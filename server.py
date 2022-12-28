import pandas as pd
import sqlalchemy
import datetime

engine = sqlalchemy.create_engine('mysql+pymysql://sql10586529:dCAVRa116V@sql10.freesqldatabase.com/sql10586529')
# engine = sqlalchemy.create_engine('mysql+pymysql://<username>:<password>@<host>/<dbname>')

# engine.execute(f'''
#     CREATE TABLE px_tickers (
#         rptdt DATE NOT NULL, 
#         ticker VARCHAR(12) NOT NULL,
#         field VARCHAR(12) NOT NULL,
#         value FLOAT(18,5) NOT NULL,
#         PRIMARY KEY (rptdt, ticker, field)
#     )
#    ''')

# engine.execute('DELETE FROM px_tickers')


# today = datetime.date.today()

# for i in range(1000):
#     engine.execute(f'''
#         INSERT INTO px_tickers (rptdt, ticker, field, value)
#         VALUES ('{(today+datetime.timedelta(days=i)).strftime('%Y-%m-%d')}', 'JBSS3 Equity', 'px_last', {i})
#     ''')
#     print(i)
now = datetime.datetime.now()

df = pd.read_sql(f'''
    SELECT rptdt, value FROM px_tickers
    WHERE rptdt >= '2025-01-01'
''', engine)

print(datetime.datetime.now()-now)

print(df)