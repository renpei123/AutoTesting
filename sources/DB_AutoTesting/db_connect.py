import pyodbc
import json



def get_connStr(uid,pwd,db):
	with open('C:/Users/RongHe/AutoTest/Conf/db_info.json','r',encoding = 'utf-8') as f:
		config = json.load(f)
	if db == 'pda':
		driver = config[db]["driver"]
		hostname = config[db]["host"]
		port = config[db]["port"]
		database = config[db]["database"]
		username = uid
		password = pwd
		connStr = 'DRIVER='+driver + ';' + 'SERVER='+hostname + ';' +'PORT='+ port + ';' + 'DATABASE='+database + ';' + 'UID='+username + ';' +'PWD='+ password
	elif db == 'db2':
		driver = config[db]["driver"]
		hostname = config[db]["host"]
		port = config[db]["port"]
		database = config[db]["database"]
		username = uid
		password = pwd
		connStr = 'DRIVER='+driver + ';' + 'HOSTNAME='+hostname + ';' +'PORT='+ port + ';' + 'DATABASE='+database + ';' + 'UID='+username + ';' +'PWD='+ password    
	return connStr

def conn_odbc_db2():
    connStr=get_connStr('pdaetlg','dec10dec','db2')
    conn = pyodbc.connect(connStr)
    cursor =conn.cursor()
    cursor.execute("select * from BMSIW.T510EMF")   
    result =cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def conn_odbc_pda():
    conStr=get_connStr('siwsit','oct18oct','pda')
    conn =  pyodbc.connect(conStr)
    cursor =conn.cursor()
    cursor.execute("select count(*) from RDMSTG.SERVICE_LINE;")
    result =cursor.fetchall()
    conn.close()
    return result

def exec_sql_pda(id,pwd,objectList):
    
    conStr=get_connStr(id,pwd,'pda')
    #print(conStr)
    conn =  pyodbc.connect(conStr)
    cursor =conn.cursor()
    result = {}
    for obj in objectList:
        print("validating "+obj +"...")
        sql = "select count(*) from " + obj
        try:
            cursor.execute(sql)
            table =cursor.fetchall()
            count = table[0][0]
            result[obj]=count
        except pyodbc.Error as e:
            #print(type(e))
            #reportList.append(obj+","+ err)
            #reportList.append(obj+","+str(e.args[1]))
            result[obj]=str(e.args[1])
            continue            
        else:
            continue
    conn.close()
    #print(result)
    return result



def main():
    #access db2 and print rows for a table
    #data=conn_odbc_db2()
    #for i in data:
     #   print("员工工号是：",list(i)[0]," 员工工资是：",list(i)[5])

    #access pda and print rows for a table
    #data = conn_odbc_db2()
    #for i in data:
    #    print(list(i))

    #pdadata = exec_sql_pda('twwview','oct18oct',['BDWDB.CHRG_DTL18'])
	db2data = conn_odbc_db2()
	print(db2data)


if __name__ == "__main__":
    main()