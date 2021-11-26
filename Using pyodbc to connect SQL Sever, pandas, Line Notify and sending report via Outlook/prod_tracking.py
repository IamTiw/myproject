import pyodbc
import string
from datetime import datetime, timedelta
from prod_setup import *

server = 'Your IP, Port' #<<<<<<<<<<<<<<<<<<<<<<<<< [1/5]
database = 'Database name' #<<<<<<<<<<<<<<<<<<<<<<<<< [2/5]
username = 'User' #<<<<<<<<<<<<<<<<<<<<<<<<< [3/5]
password = 'Password' #<<<<<<<<<<<<<<<<<<<<<<<<< [4/5]
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)
query = "Query" #<<<<<<<<<<<<<<<<<<<<<<<<< [5/5]
# "SELECT DISTINCT REPLACE(REPLACE(REPLACE(REPLACE(PDHS_LOG.dbo.Log_Status.TestStation,10613,'Round Column'),11002,'Beam'),189,'Cantilever Setpack'),18056,'DL-Plus 1') AS ProductionLine, CONVERT(date,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)) AS Date, DATEPART(HOUR,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)) AS Hourly, COUNT(CONCAT(PDHS_LOG.dbo.Log_Status.PoNo,PDHS_LOG.dbo.Log_Status.Serial ,PDHS_LOG.dbo.Log_Status.Status)) AS Qty FROM PDHS_LOG.dbo.Log_Status INNER JOIN PDHS_LOG.dbo.Log_DATETIME ON PDHS_LOG.dbo.Log_DATETIME.SetID = PDHS_LOG.dbo.Log_Status.SetID WHERE CONVERT(date,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)) = CONVERT(date,GETDATE()) AND DATEPART(HOUR,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)) = DATEPART(Hour,DATEADD(HOUR,5,GETDATE())) AND PDHS_LOG.dbo.Log_Status.TestStation IN (18056,11002,189,10613) AND PDHS_LOG.dbo.Log_Status.Status IN (1) GROUP BY PDHS_LOG.dbo.Log_Status.TestStation, CONVERT(date,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)), DATEPART(HOUR,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)),PDHS_LOG.dbo.Log_Status.Status"
cursor = cnxn.cursor()

day_shift = list(range(8, 20))
night_shift = list(range(0, 8))
data = []

for row in cursor.execute(query):
    prod_line = row[0]
    date_today = row[1].format('%Y-%m-%d')
    start_time = f'{row[2]:.2f}'
    stop_time = f'{row[2]+1:.2f}'
    total_good = row[3]

    if row[2] in day_shift:
        shift_name = "Day"
    else:
        shift_name = "Night"

    if row[2] in night_shift:
        cal_date = datetime.strptime(row[1], '%Y-%m-%d')
        cal_date = cal_date - timedelta(days=1)
        shift_date = cal_date.strftime('%Y-%m-%d')
    else:
        shift_date = row[1]

    prefix = string.ascii_lowercase
    period_time = f'[{prefix[row[2]]}] {str(start_time)} - {str(stop_time)}'
    datasets = [prod_line, date_today,
                period_time, total_good, shift_name, shift_date]
    CsvDatabase.update_csv(datasets)

    data.append(
        f'\nLine: {prod_line}'
        f'\nGood: {total_good}\n')

data_format = [
    f'\n#Hourly Report\nDate: {date_today}'
    f'\nTime: {start_time} - {stop_time}\n'
]

data_format.extend(data)
data_format = ConvertText.convert_list_to_string(data_format)
Notify.prod_notify(data_format)
