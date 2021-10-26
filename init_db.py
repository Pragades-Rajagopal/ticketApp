import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as data:
    conn.executescript(data.read())

cur = conn.cursor()

# Test insertion
cur.execute("insert into tickets (TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON) values (?,?,?,?,?,?)", (9676439, 'REPC-Cramer Job failure', 'Incident', 'NA', '2021/09/24 14:57:27', 'Sep2021'))
cur.execute("insert into tickets (TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON) values (?,?,?,?,?,?)", (9686631, 'Pilot activity-Owner/Service Configuration', 'Service Request', 'Once Pilot is identified, these request will not flow into L2 bucket', '2021/09/10 14:57:27', 'Sep2021'))

conn.commit()
conn.close()

