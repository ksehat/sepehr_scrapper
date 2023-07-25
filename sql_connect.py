import pyodbc

server = '192.168.40.57'
database = 'fids_mongodb'
username = 'k.sehat'
password = 'K@123456'
cnxn = pyodbc.connect(driver='{SQL Server}',
                      server=server,
                      database=database,
                      uid=username, pwd=password)
cursor = cnxn.cursor()

# Define the INSERT statement
insert_stmt = "INSERT INTO FIDS_JSON (jsoncontent,SiteName) VALUES (?,?)"

# Execute the INSERT statement
cursor.execute(insert_stmt, ('kanan3','sitename'))

# Commit the changes
cnxn.commit()

# Close the connection
cnxn.close()