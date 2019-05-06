import ibm_db


#conn = ibm_db.connect("DATABASE=ONETEAMP;HOSTNAME=b03acirdb051.ahe.boulder.ibm.com;PORT=60015;PROTOCOL=TCPIP;UID=*****;PWD=*****;SECURITY=SSL;SSLCLIENTKEYSTOREDB=C:\Users\FuLiQu\Documents\SSL\db2_ssl_keydb.kdb;SSLCLIENTKEYSTASH=C:\Users\FuLiQu\Documents\SSL\db2_ssl_keydb.sth;", "", "")

conn = ibm_db.connect("DATABASE=ONETEAMP;HOSTNAME=b03acirdb051.ahe.boulder.ibm.com;PORT=60027;PROTOCOL=TCPIP;UID=*****;PWD=*****;", "", "")

if conn:
    sql = "SELECT app_code,name from appl.application FETCH FIRST  10 rows ONLY "
    stmt = ibm_db.exec_immediate(conn, sql)
    result = ibm_db.fetch_both(stmt)
    while(result):
        #print(result[0],result[1]) CV,,,,,,,,,,,,,,,;[;[           MMMM GB C
        print(result)
        result = ibm_db.fetch_both(stmt)
ibm_db.free_stmt(stmt)
ibm_db.close(conn)

