import pyodbc
import os
import configparser
from cryptography.fernet import Fernet


def strDecrypt(cipherText,cipher):
    str=cipher.decrypt(cipherText)
    return str

def get_connStr(db):
    cur_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(cur_path, 'db.info')
    conf = configparser.ConfigParser()
    conf.read(config_path)
    cipher_key = b'nkr_hFoPzlhB4XPegNMRubCar3bezyNcxVqx116Avao='
    cipher = Fernet(cipher_key)
    if db == 'db2':
        driver = conf.get(db, 'driver')
        hostname = conf.get(db,  'hostname')
        port = conf.get(db, 'port')
        database = conf.get(db, 'database')
        username = conf.get(db, 'username')
        password = strDecrypt(conf.get(db, 'password').encode('utf-8'),cipher).decode('utf-8')
        #print(password)
        connStr = 'DRIVER='+driver + ';' + 'HOSTNAME='+hostname + ';' +'PORT='+ port + ';' + 'DATABASE='+database + ';' + 'UID='+username + ';' +'PWD='+ password
    elif db == 'mysql':
        connStr = ''
    elif db == 'PDA':
        driver = conf.get(db, 'driver')
        hostname = conf.get(db, 'hostname')
        port = conf.get(db, 'port')
        database = conf.get(db, 'database')
        username = conf.get(db, 'username')
        password = strDecrypt(conf.get(db, 'password').encode('utf-8'), cipher).decode('utf-8')
        connStr = 'DRIVER='+driver + ';' + 'SERVER='+hostname + ';' +'PORT='+ port + ';' + 'DATABASE='+database + ';' + 'UID='+username + ';' +'PWD='+ password
    else:
        connStr = ''
    return connStr

def conn_odbc_db2():
    #windows下使用odbc dsn的方式连接db2 sample数据库
    #conn = pyodbc.connect('DSN=sample;PWD=sqlee23-')
    #windows下使用odbc driver的方式连接db2sample数据库
    connStr=get_connStr('db2')
    conn = pyodbc.connect(connStr)
    cursor =conn.cursor()
    cursor.execute("select * from staff where id < 30")
    result =cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def conn_odbc_pda():
    #windows下使用odbc dsn的方式连接pda数据库
    conStr=get_connStr('PDA')
    #print(conStr)
    conn =  pyodbc.connect(conStr)
    #conn = pyodbc.connect('DSN=NZSQL;PWD=aug18aug')
    cursor =conn.cursor()
    cursor.execute("select count(1) from CISFSTG.DUNS_tmp")
    result =cursor.fetchall()
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

    pdadata = conn_odbc_pda()
    for i in pdadata:
        print(list(i))


if __name__ == "__main__":
    main()