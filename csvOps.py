import pandas as pd
import sqlite3
import os

save_path = '.\exports'

def getAll(cur_date):

    file_name = 'data_'+cur_date+'.csv'
    value = os.path.join(save_path, file_name)

    conn = sqlite3.connect('database.db', isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)
    data = pd.read_sql_query('select * from tickets order by TICKET desc', conn)
    data.to_csv(value, index=False)
    conn.close()


def getMonthData(month, cur_date):
    
    file_name = 'data_'+month+'_'+cur_date+'.csv'
    value = os.path.join(save_path, file_name)

    conn = sqlite3.connect('database.db', isolation_level=None,
    detect_types=sqlite3.PARSE_COLNAMES)
    data = pd.read_sql_query('select * from tickets order by TICKET desc',  conn)
    data = data[data.MON == month]
    data.to_csv(value, index=False)
    conn.close()

