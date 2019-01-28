import pyodbc
from Read_conf import ReadConfig
import ibm_db



def get_connStr(uid,pwd,db_node):
    conf = ReadConfig()
    db = conf.Read_db_config(db_node)
    print(db)
    if db['db_type'] == 'db2':
        con_str = "DATABASE={};HOSTNAME={};PORT={};PROTOCAL={};UID={};PWD={}".format(db['database'],db['hostname'],db['port'],db['protocal'],uid,pwd)
        print(con_str)
    elif db['driver'] == '{IBM DB2 ODBC DRIVER}':
        con_str = "DRIVER={};DATABASE={};HOSTNAME={};PORT={};UID={};PWD={}".format(db['driver'],db['database'],db['hostname'],db['port'],uid,pwd)
        print(con_str)
    elif db['driver'] == '{NetezzaSQL}':
        con_str = "DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}".format(db['driver'],db['hostname'],db['port'],db['database'],uid,pwd)
        print(con_str)
    else:
        con_str = ''
        print(con_str)
    return con_str

def conn_odbc_db2():
    connStr=get_connStr('db2')
    conn = pyodbc.connect(connStr)
    cursor =conn.cursor()
    cursor.execute("select * from staff where id < 30")   
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

def exec_sql_pda(db_node,id,pwd,sql):
    
    conStr=get_connStr(id,pwd,db_node)
    #print(conStr)
    conn =  pyodbc.connect(conStr)
    cursor =conn.cursor()
    table = []
    try:
        cursor.execute(sql)
        table =cursor.fetchall()
    except pyodbc.Error as e:
        #print(type(e))
        #reportList.append(obj+","+ err)
        #reportList.append(obj+","+str(e.args[1]))
        print(e.args)
    finally:
        conn.close()
        #print(result)
        return table


def exec_sql_db2(driver_node, id, pwd, query):
    conStr = get_connStr(id, pwd, driver_node)
    conn = None
    try:
        conn = ibm_db.connect(conStr, "", "")
        stmt = ibm_db.exec_immediate(conn, query)
        if __name__ == '__main__':
            rows = ibm_db.fetch_both(stmt)
            print(rows)
    except Exception as e:
        print(e.args)
    finally:
        conn.close()
    return rows

def exec_sql_odbc_db2(uid,pwd,db_node,query):
    connStr=get_connStr('siwwebd','Bluemix_jan18jan','bluedb2')
    conn = pyodbc.connect(connStr)
    cursor =conn.cursor()
    cursor.execute(query)
    result =cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def exec_sql_common(db_node,id,pwd,query):
    connStr=get_connStr(id,pwd,db_node)
    conn = pyodbc.connect(connStr)
    try:
        cursor =conn.cursor()
        cursor.execute(query)
        info = cursor.description
        rs =cursor.fetchall()
        result = []
        for line in rs:
            row = dict()
            for column in info:
                column_name = column[0]
                gen_str = "line."+column_name
                value = eval(gen_str)
                row[column_name] = value
            result.append(row)
    except Exception as e:
        print(e.args)
    finally:
        cursor.close()
        conn.close()
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
    #print(get_connStr('siwsit','nov18nov','siwods'))
    #print(get_connStr('siwwebd','Bluemix_jan18jan','bluedb2'))
    #rs = exec_sql_db2('siwdb2', 'pdaetlg', 'dec10dec', 'select * from BMSIW.T510EMF')

    #rs = exec_sql_db2('bluedb2', 'siwwebd', 'Bluemix_jan18jan', 'select * from XLSSTG.LOAD_APPLICATION')
    #rs = exec_sql_odbc_db2('bluedb2', 'siwwebd', 'Bluemix_jan18jan', 'select * from XLSSTG.LOAD_APPLICATION')
    rs = exec_sql_common('bluedb2','siwwebd', 'Bluemix_jan18jan', 'select * from XLSSTG.LOAD_APPLICATION')
    print(rs)


if __name__ == "__main__":
    main()