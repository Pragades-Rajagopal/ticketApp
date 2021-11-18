import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as data:
    conn.executescript(data.read())

cur = conn.cursor()

# Test insertion
cur.execute("insert into tickets (APP_NM, TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON, RESOLVED_BY) values (?,?,?,?,?,?,?,?)", ('TIGER', 10033917, 'REPC-Cramer Job failure', 'Incident', 'NA', '2021/10/01 14:57:27', 'Oct2021', 'Sucharitha'))
cur.execute("insert into tickets (APP_NM, TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON, RESOLVED_BY) values (?,?,?,?,?,?,?,?)", ('REPC', 10033918, 'Pilot activity-Owner/Service Configuration', 'Service Request', 'Once Pilot is identified, these request will not flow into L2 bucket', '2021/11/02 14:57:30', 'Nov2021', 'Bharat'))

conn.commit()
conn.close()

