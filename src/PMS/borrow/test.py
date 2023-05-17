import pyodbc

conn = pyodbc.connect("DRIVER={{SQL Server}};SERVER={server}; database={database}; \
                   trusted_connection=yes;UID={uid};PWD={pwd}".format(server="10.96.101.4", database="EFGP_Test", uid="sa", pwd="134"))
sql = """select id,organizationUnitName 
             from OrganizationUnit where validType = 1 and managerOID is not null order by id"""

cur = conn.cursor()
cur.execute(sql)
cur.fetchall()