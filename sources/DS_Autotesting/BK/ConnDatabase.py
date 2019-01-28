import os
import configparser
import pyodbc

def conn_Database(db,dbtype):
    cur_path = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(cur_path, 'db.ini')
    conf = configparser.ConfigParser()
    conf.read(config_path)

    if dbtype.upper() == 'DB2':
        driver = conf.get(db, 'driver')
        hostname = conf.get(db, 'hostname')
        port = conf.get(db, 'port')
        database = conf.get(db, 'database')
        username = conf.get(db, 'username')
        password = conf.get(db, 'password')
        # print(password)
        connStr = 'DRIVER=' + driver + ';' + 'HOSTNAME=' + hostname + ';' + 'PORT=' + port + ';' + 'DATABASE=' + database + ';' + 'UID=' + username + ';' + 'PWD=' + password
    elif dbtype.upper() == 'PDA':
        driver = conf.get(db, 'driver')
        hostname = conf.get(db, 'hostname')
        port = conf.get(db, 'port')
        database = conf.get(db, 'database')
        username = conf.get(db, 'username')
        password = conf.get(db, 'password')
        connStr = 'DRIVER=' + driver + ';' + 'SERVER=' + hostname + ';' + 'PORT=' + port + ';' + 'DATABASE=' + database + ';' + 'UID=' + username + ';' + 'PWD=' + password
    else:
        connStr = ''

constr = "DRIVER={IBM DB2 ODBC DRIVER};HOSTNAME=dashdb-txn-small-yp-dal09-70.services.dal.bluemix.net;PORT=50000;DATABASE=BLUDB;UID=siwwebd;PWD=Bluemix_jan18jan"
conn = pyodbc.connect(constr)
    

