import pyodbc
from Read_conf import ReadConfig
import ibm_db


def get_connStr(uid, pwd, db_node):
    conf = ReadConfig()
    db = conf.Read_db_config(db_node)
    if db['driver'] == '{IBM DB2 ODBC DRIVER}':
        con_str = "DRIVER={};DATABASE={};HOSTNAME={};PORT={};UID={};PWD={}".format(db['driver'],db['database'],db['hostname'],db['port'],uid,pwd)
    elif db['driver'] == '{NetezzaSQL}':
        con_str = "DRIVER={};SERVER={};PORT={};DATABASE={};UID={};PWD={}".format(db['driver'],db['hostname'],db['port'],db['database'],uid,pwd)
    else:
        con_str = ''
    return con_str


'''this function will connect to the db which defined by db_node,
run the select query then output the dict list which is a table like structure
'''


def exec_sql_common(db_node, id, pwd, query):
    connStr = get_connStr(id, pwd, db_node)
    print("Connection String:%s" % connStr)
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
    rs = exec_sql_common('bluedb2','siwwebd', 'Bluemix_jan18jan', 'select * from XLSSTG.LOAD_STATUS')
    #rs = exec_sql_common('siwodspda', 'siwsit', 'oct18oct', 'select * from ACCTRCVBL.BILLING_ITEM')
    print(rs)


if __name__ == "__main__":
    main()