import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as data:
    conn.executescript(data.read())

cur = conn.cursor()

# Test insertion
cur.execute("insert into tickets (APP_NM, TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON) values (?,?,?,?,?,?,?)", ('TIGER', 9676439, 'REPC-Cramer Job failure', 'Incident', 'NA', '2021/10/05 14:57:27', 'Oct2021'))
cur.execute("insert into tickets (APP_NM, TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON) values (?,?,?,?,?,?,?)", ('REPC', 9686631, 'Pilot activity-Owner/Service Configuration', 'Service Request', 'Once Pilot is identified, these request will not flow into L2 bucket', '2021/11/08 14:57:27', 'Nov2021'))

conn.commit()
conn.close()

