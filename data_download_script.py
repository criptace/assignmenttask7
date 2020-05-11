import uuid
import datefinder as datefinder
import pyodbc as pyodbc
import requests

endpoint_url = 'https://api.covid19api.com/country/malta'
response = requests.get(endpoint_url)
json_response = response.json()

server = 'tcp:SQL-SRV-01'
database = 'coviddata'
username = 'sa'
password = 'Pa$$w0rd'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

cursor.execute("delete from tblDailyStats")

for day in json_response:
    confirmed = day['Confirmed']
    deaths = day['Deaths']
    active = day['Active']
    recovered = day['Recovered']

    matches = datefinder.find_dates(day['Date'])
    date = None

    for match in matches:
        date = match
        break
    cursor.execute("""
    INSERT INTO tblDailyStats(id, date, confirmed, active, recovered, deaths) values (?,?,?,?,?,?)
    """, uuid.uuid1(), date, confirmed, active, recovered, deaths)
    cnxn.commit()

cnxn.close()
