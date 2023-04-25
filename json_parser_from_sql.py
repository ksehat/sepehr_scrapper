import pyodbc, ast, json

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=192.168.20.237;DATABASE=GriffinDW_Stage;UID=sa;PWD=Sep@1401')
cursor = cnxn.cursor()

cursor.execute("SELECT * FROM [GriffinDW_Stage].[dbo].[RouteMonitoringResult]")

rows = cursor.fetchall()

for row in rows:
    json_parsed = json.dumps(ast.literal_eval((row[4]).decode('utf-8')))
    cursor.execute(f"Update [GriffinDW_Stage].[dbo].[RouteMonitoringResult] set Json_Parsed = {json_parsed},[Update] = 1 where RouteMonitoringResult = {row[0]}" )
cursor.close()
cnxn.close()
