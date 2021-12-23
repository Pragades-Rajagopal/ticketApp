from sqlite3.dbapi2 import OperationalError, IntegrityError
from flask import Flask, render_template, request, flash, send_file, redirect, url_for
import sqlite3
import time, datetime
from flask.wrappers import Response
from csvOps import getAll, getMonthData
from werkzeug.exceptions import abort
import pandas as pd
import numpy as np
import csv


today = datetime.date.today()
first = today.replace(day=1)
lastMonth = (first - datetime.timedelta(days=1)).strftime("%b%Y") 

app = Flask(__name__)

app.config.from_pyfile('session_key.py')

def database_connection():
    conn = sqlite3.connect('database.db', timeout=1)
    conn.row_factory = sqlite3.Row
    return conn

def close_db_connection():
    conn = sqlite3.connect('database.db')
    conn.close()

def check(num):

    conn = database_connection()
    value = conn.execute('select TICKET from tickets where TICKET = ?', (num,)).fetchone()
    conn.close()

    return value

def getCount():
    m = str(time.strftime("%b%Y", time.gmtime()))

    conn = sqlite3.connect('database.db', isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES, timeout=1)
    data = pd.read_sql_query('select TICKET_TYPE, MON from tickets', conn)
    conn.close()
    incident = np.sum((data.TICKET_TYPE == 'Incident') & (data.MON == m))
    req = np.sum((data.TICKET_TYPE == 'Service Request') & (data.MON == m))
    return {'incident':incident, 'req':req}


@app.route('/ticket-tool/csv_lastMonth')
def getCSVmonth():

    cur_date = str(time.strftime("%Y%m%d_%H%M", time.gmtime()))
    getMonthData(str(lastMonth), cur_date)

    return send_file('./exports/data_'+lastMonth+'_'+cur_date+'.csv',
    mimetype='text/csv',
    download_name='data_'+lastMonth+'_'+cur_date+'.csv',
    as_attachment=True)



@app.route('/ticket-tool/getCSVfile')
def getCSV():

    cur_date = str(time.strftime("%Y%m%d_%H%M", time.gmtime()))
    getAll(cur_date)

    return send_file('./exports/data_'+cur_date+'.csv',
    mimetype='text/csv',
    download_name='data_'+cur_date+'.csv',
    as_attachment=True)


@app.route('/ticket-tool', methods=('GET', 'POST'))
def index():

    close_db_connection()

    try:
 
        if request.method == 'POST':
            num = request.form['num']
            descr = request.form['descr']
            ttype = request.form.get('ticket_type')
            detail = request.form['detail']
            app_name = request.form.get('app_name')
            resolved_by = request.form.get('resolved_user')

            created_on = str(time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()))
            mon = str(time.strftime("%b%Y", time.gmtime()))

            value = check(num)

            if not num:
                flash('Ticket number is required')
            elif not descr:
                flash('Description is required')
            elif not detail:
                flash('Detailed description is required. If not, NA')
            elif value is not None:
                # print('TT already exists')
                abort (Response('''<H1>Ticket already exists</H1>
                <br>
                <a href="/ticket-tool">GO HOME</a>'''))

            else:
                conn = database_connection()
                conn.execute('insert into tickets (APP_NM, TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON, RESOLVED_BY) values (?,?,?,?,?,?,?, ?)', (app_name ,num, descr, ttype, detail, created_on, mon, resolved_by))
                conn.commit()
                conn.close()

                return redirect(url_for('index'))

        x = getCount()

        app_nm = [{'name':'REPC'}, {'name':'TIGER'}, {'name':'RERT'}, {'name':'MSPS'}, {'name':'REACT'}]
        users = [{'user':'Bharat'}, {'user':'Harish'}, {'user':'Pragadeswar'}, {'user':'Saibhargavi'}, {'user':'Sucharitha'}, {'user':'Surandranath'}]

        a = []
        with open('./category/ticket_category.csv', 'r') as value:
            a = [{k: v for k, v in row.items()} 
                for row in csv.DictReader(value, skipinitialspace=True)]

        close_db_connection()
        return render_template('index.html', data=[{'name':'Incident'}, {'name':'Service Request'}], app_nm=app_nm, count=x, lastMonth=lastMonth, users=users, category=a)

    except OperationalError or IntegrityError as e:
        close_db_connection()
        abort (Response('''<H1>Ticket Number should be a number or Something went wrong!</H1>
                <br>
                <a href="/ticket-tool">GO HOME</a>'''))

    # except IntegrityError as e:
    #     close_db_connection()
    #     abort (Response('''<H1>Ticket Number should be a number or Something went wrong!</H1>
    #             <br>
    #             <a href="/">GO HOME</a>'''))


@app.route('/ticket-tool/search', methods = ['POST', 'GET'])
def search():
    
    try:
        
        text = request.form['tt_number']
        conn = database_connection()
        cur = conn.cursor()
        post = cur.execute("SELECT * from tickets where ticket=?",(text,)).fetchone()
        conn.commit()
        conn.close()

        if post is None:
            return redirect(url_for('index'))

        return render_template('search.html', post=post)

    except TypeError as e:
        close_db_connection()
        abort (Response('''<H1>Ticket does not exist!!</H1>
        <br>
        <a href="/ticket-tool">GO HOME</a>'''))



# app.run(port=5000, host='localhost', debug=True)
app.run(debug=True)


