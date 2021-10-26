from sqlite3.dbapi2 import OperationalError, IntegrityError
from flask import Flask, render_template, request, flash, send_file, redirect, url_for
import sqlite3
import time, datetime
from flask.wrappers import Response
from csvOps import getAll, getMonthData
from werkzeug.exceptions import abort


today = datetime.date.today()
first = today.replace(day=1)
lastMonth = (first - datetime.timedelta(days=1)).strftime("%b%Y") 

app = Flask(__name__)

app.config.from_pyfile('session_key.py')

def database_connection():
    conn = sqlite3.connect('database.db', timeout=2)
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

@app.route('/csv_lastMonth')
def getCSVmonth():

    cur_date = str(time.strftime("%Y%m%d_%H%M", time.gmtime()))
    getMonthData(str(lastMonth), cur_date)

    return send_file('./exports/data_'+lastMonth+'_'+cur_date+'.csv',
    mimetype='text/csv',
    download_name='data_'+lastMonth+'_'+cur_date+'.csv',
    as_attachment=True)



@app.route('/getCSVfile')
def getCSV():

    cur_date = str(time.strftime("%Y%m%d_%H%M", time.gmtime()))
    getAll(cur_date)

    return send_file('./exports/data_'+cur_date+'.csv',
    mimetype='text/csv',
    download_name='data_'+cur_date+'.csv',
    as_attachment=True)


@app.route('/', methods=('GET', 'POST'))
def index():

    close_db_connection()

    try:
 
        if request.method == 'POST':
            num = request.form['num']
            descr = request.form['descr']
            ttype = request.form.get('ticket_type')
            detail = request.form['detail']

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
                print('TT already exists')
                abort (Response('''<H1>Ticket already exists</H1>
                <br>
                <a href="/">GO HOME</a>'''))

            else:
                conn = database_connection()
                conn.execute('insert into tickets (TICKET, RESOLUTION, TICKET_TYPE, COMMENT, CREATED_ON, MON) values (?,?,?,?,?,?)', (num, descr, ttype, detail, created_on, mon))
                conn.commit()
                conn.close()

                return redirect(url_for('index'))

        close_db_connection()
        return render_template('index.html', data=[{'name':'Incident'}, {'name':'Service Request'}], lastMonth=lastMonth)

    except OperationalError or IntegrityError as e:
        close_db_connection()
        abort (Response('''<H1>Ticket Number should be a number or Something went wrong!</H1>
                <br>
                <a href="/">GO HOME</a>'''))

    # except IntegrityError as e:
    #     close_db_connection()
    #     abort (Response('''<H1>Ticket Number should be a number or Something went wrong!</H1>
    #             <br>
    #             <a href="/">GO HOME</a>'''))


# app.run(port=5000, host='localhost')


