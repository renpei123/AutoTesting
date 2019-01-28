from script import ConnDatabase



def get_row_count(db,dbtype,tablist):
    conn=ConnDatabase.conn_Database(db,dbtype)
    cursor = conn.cursor()
    cursor.execute("select count(1) from  "+tablist)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_sample_date(db,dbtype,tablist):
    conn=ConnDatabase.conn_Database(db,dbtype)
    cursor = conn.cursor()
    cursor.execute("select * from  "+ tablist +" fetch first 5 rows only")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_table_structure(db,dbtype,tablist):
    conn=ConnDatabase.conn_Database(db,dbtype)
    cursor = conn.cursor()
    if dbtype.upper()=='DB2':
        cursor.execute("select name,coltype,length,nulls from SYSIBM.SYSCOLUMNS where tbname = 'T510EMF'")
    elif dbtype.upper()=='PDA':
        cursor.execute("SELECT ATTNAME,FORMAT_TYPE,ATTCOLLENG,ATTNOTNULL "
                        +"FROM _V_RELATION_COLUMN "
                       +"WHERE UPPER(TYPE) = 'TABLE' "
                         +"AND UPPER(SCHEMA) = UPPER('AGREEMENT')"
                         +"AND UPPER(NAME) = UPPER('EMPLOYEE_INFORMATION_REFERENCE') ")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def main():


    source_db,source_tab='siwdb2','T510EMF'
    target_db,target_tab='siwods','AGREEMENT.EMPLOYEE_INFORMATION_REFERENCE'


    #compare table structure
    v_source_strct=get_table_structure(source_db,'db2',source_tab)
    print(v_source_strct)
    for i in v_source_strct:
        print("there are "+str(len(list(v_source_strct)))+' columns:'+str(list(i)))
    print("######")
    v_target_strct = get_table_structure(target_db, 'pda', target_tab)
    for j in v_target_strct:
        print("there are "+str(len(list(v_target_strct)))+' columns,curently it is: '+str(list(j)))





    """
    #
    #compare data total rows.
    #
    
    #v_source_rows = get_row_count(source_db,'DB2',source_tab)
    #print("the total rows of soure table: "+str(v_source_rows[0][0]))


    #v_target_rows = get_row_count(target_db,'PDA',target_tab)
    #print("the total rows of target table: "+str(v_target_rows[0][0]))

    #if v_target_rows[0][0] != v_source_rows[0][0]:
    #    v_gap=v_source_rows[0][0] - v_target_rows[0][0]
    #    print("the gap between source and target table is:"+str(abs(v_gap)))
    """












if __name__ == "__main__":
    main()