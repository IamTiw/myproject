import pyodbc
from line_notify import Notify

server = '192.168.81.7,1433'
database = 'PDHS_LOG'
username = 'plcsql'
password = '9191'
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD=' + password)
query = "SELECT DISTINCT REPLACE(REPLACE(REPLACE(REPLACE(PDHS_LOG.dbo.Log_Status.TestStation,10613,'Round Column'),11002,'Beam'),189,'Cantilever Setpack'),18056,'DL-Plus 1') AS ProductionLine, CONVERT(date,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)) AS Date, DATEPART(HOUR,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)) AS Hourly, COUNT(CONCAT(PDHS_LOG.dbo.Log_Status.PoNo,PDHS_LOG.dbo.Log_Status.Serial ,PDHS_LOG.dbo.Log_Status.Status)) AS Qty FROM PDHS_LOG.dbo.Log_Status INNER JOIN PDHS_LOG.dbo.Log_DATETIME ON PDHS_LOG.dbo.Log_DATETIME.SetID = PDHS_LOG.dbo.Log_Status.SetID WHERE CONVERT(date,PDHS_LOG.dbo.Log_DATETIME.ParamValue) = CONVERT(date,GETDATE()) AND DATEPART(HOUR,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)) = DATEPART(Hour,DATEADD(HOUR,5,GETDATE())) AND PDHS_LOG.dbo.Log_Status.TestStation IN (18056,11002,189,10613) AND PDHS_LOG.dbo.Log_Status.Status IN (1) GROUP BY PDHS_LOG.dbo.Log_Status.TestStation, CONVERT(date,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)), DATEPART(HOUR,DATEADD(HOUR,6,PDHS_LOG.dbo.Log_DATETIME.ParamValue)),PDHS_LOG.dbo.Log_Status.Status"
cursor = cnxn.cursor()

for row in cursor.execute(query):
    prod_line = row[0]
    date_today = row[1]
    start_time = f'{row[2]:.2f}'
    stop_time = f'{row[2]+1:.2f}'
    total_good = row[3]
    Notify.prod_notify(prod_line,date_today,start_time,stop_time,total_good)
