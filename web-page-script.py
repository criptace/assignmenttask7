import pyodbc as pyodbc
from flask import Flask
from flask import render_template

server = 'tcp:SQL-SRV-01'
database = 'coviddata'
username = 'sa'
password = 'Pa$$w0rd'


app = Flask(__name__)

@app.route('/')
def hello():
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    rows = cursor.execute("SELECT id, date, confirmed, active, recovered, deaths FROM tblDailyStats ORDER BY date DESC").fetchall()
    return render_template('list-cases.html', rows=rows)
    cnxn.close()

if __name__ == '__main__':
    app.run()
