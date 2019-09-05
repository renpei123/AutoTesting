import pyodbc
from Common.Read_conf import ReadConfig
import os
import json

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
    print("Connection String:%s" % connStr.replace(pwd, '********'))
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
                row[column_name] = str(value)
            result.append(row)
    except Exception as e:
        print(e.args)
    finally:
        cursor.close()
        conn.close()
    return result

def exec_sql_with_jdbc(db_node,user,pwd,query):
    conf = ReadConfig()
    db = conf.Read_db_config(db_node)
    jdbc_driver = db['driver']
    jdbc_url = db['url']
    jdbc_user = user
    jdbc_pwd = pwd
    jdbc_query = '"'+query+'"'
    java_path = conf.Read_Java_home()
    current_path = os.path.dirname(os.path.realpath(__file__))
    JDBC_path = os.path.join(current_path,'../JDBC/Query_JDBC.jar')
    command = java_path + '/java -jar ' + JDBC_path + ' '+jdbc_driver+' '+jdbc_url+' '+jdbc_user+' '+jdbc_pwd+' '+jdbc_query
    print("\tRunning Command:"+command)
    rs = os.popen(cmd=command, mode='r')
    query_result = json.loads(rs.readlines()[0])
    return query_result
    #print(query_result)

def main():
    #rs = exec_sql_common('bluedb2','siwwebd', 'Bluemix_jan18jan', 'select * from XLSSTG.LOAD_STATUS')
    rs = exec_sql_common('siwodspda', 'siwsit', 'SIWJul201'
                                                ''
                                                '9JulSIW', 'select * from ACCTRCVBL.BILLING_ITEM')
    #result_set = exec_sql_with_jdbc('siwdb2_jdbc','siwsit','mar01mar',"select * from ASCA.ASCA_CONTROL_RECORD where JOB_ID='J100105'")
    print(rs)


if __name__ == "__main__":
    main()