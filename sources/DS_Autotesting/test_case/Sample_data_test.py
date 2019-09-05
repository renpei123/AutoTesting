# -*- coding: utf-8 -*-
from Common.Read_conf import ReadConfig
import datetime
from Common import db_connect, TestException
from Common.generate_report import Generate_report
import json
import re
import os

class Sample_data_test:

    def source_condition_transfer(self,source_table_name,source_condition_str):
        source_target_column_mapping = json.load(open('../tmp/source_target_column_mapping.tmp', 'r'))
        condition_str = source_condition_str.split('order by')[0]
        orderby_str = source_condition_str.split('order by')[1]
        condition_list = re.split(r'where|and',condition_str)
        orderby_list = orderby_str.split(',')
        orderby_list[-1] = orderby_list[-1].split(' ')[0]
        source_column_list = []
        target_condition_str = source_condition_str
        for item in condition_list:
            if item.strip() != '':
                source_column = item.split('=')[0].strip()
                source_column_list.append(source_column)
        for item in orderby_list:
            if item.strip() not in source_column_list:
                source_column_list.append(item.strip())

        #print("source_column_list"+str(source_column_list))
        for item in source_column_list:
            for row in source_target_column_mapping:
                if row['SOURCE_TABLE'] == source_table_name and row['SOURCE_COLUMN'] == item:
                    target_column = row['TARGET_COLUMN']
            target_condition_str = target_condition_str.replace(item,target_column)
        #print(target_condition_str)
        return target_condition_str


    def get_case_description(testcase):
        '''decorate function'''

        def decorator(test_case_func):
            def inner(*args, **kwargs):
                if testcase == 'Sample_data':
                    rc = ReadConfig()
                    print('Sample data test case started at:%s' % datetime.datetime.now())
                    with open(rc.read_row_count_test_description(),'r',encoding='utf-8') as f:
                        description = f.read()
                    print(description)
                    return test_case_func(*args, **kwargs)
            return (inner)
        return (decorator)

    @get_case_description('Sample_data')
    def sample_data_test(self,source_db_node, source_user, source_pwd,target_db_node,target_user,target_pwd):
        print("Get necessary metadata from source and target")
        """Step 1 get source/target table list from source target table mapping"""
        db2_metadata_query = "SELECT NAME as COLUMN_NAME,TBNAME as TABLE_NAME,TBCREATOR AS TABLE_SCHEMA,COLNO AS COLUMN_NUMBER,COLTYPE AS COLUMN_TYPE,LENGTH AS COLUMN_LENGTH,KEYSEQ AS KEY_SEQ \
                            FROM SYSIBM.SYSCOLUMNS \
                            WHERE UPPER(TBNAME) IN (SELECT UPPER(NAME) FROM SYSIBM.SYSTABLES WHERE TYPE = 'T') AND \
                            UPPER(TBCREATOR) in ({}) \
                            AND UPPER (TBNAME) in ({}) order by COLNO "
        pda_metadata_query = "SELECT ATTNAME AS COLUMN_NAME,NAME AS TABLE_NAME,SCHEMA AS TABLE_SCHEMA,ATTNUM AS COLUMN_NUMBER,FORMAT_TYPE AS COLUMN_TYPE,ATTCOLLENG AS COLUMN_LENGTH,'0' AS KEY_SEQ \
                            FROM _V_RELATION_COLUMN \
                            WHERE UPPER(TYPE) = 'TABLE' AND \
                            UPPER(SCHEMA) in ({}) \
                            AND UPPER(NAME) in ({}) "

        conf = ReadConfig()
        source_target_table_mapping = conf.read_source_target_table_mapping()
        print(source_target_table_mapping)
        '''Get source and target db metadata'''
        print("Step 1: Get source table list.")
        print("Step 2: Get source tables' column list to file")
        source_schema_list = []
        target_schema_list = []
        source_table_list = []
        target_table_list = []
        for item in source_target_table_mapping:
            source_schema_list.append(item['SRC_OBJ_NM'].split('.')[0])
            source_table_list.append(item['SRC_OBJ_NM'].split('.')[1])
            target_schema_list.append(item['TRGT_TBL_NM'].split('.')[0])
            target_table_list.append(item['TRGT_TBL_NM'].split('.')[1])
        source_schema_list = list(set(source_schema_list))
        target_schema_list = list(set(target_schema_list))
        source_table_list = list(set(source_table_list))
        target_table_list = list(set(target_table_list))
        print("Step 3: Get target table list.")

        '''get source tables' metadata'''
        source_db_driver = conf.Read_db_config(source_db_node)['driver']
        #db_driver = db_node['driver']
        if source_db_driver == '{IBM DB2 ODBC DRIVER}' or source_db_driver == 'com.ibm.db2.jcc.DB2Driver':
            source_query =db2_metadata_query.format(str(source_schema_list).strip('[').strip(']'),str(source_table_list).strip('[').strip(']'))
            print(source_query)
        else:
            source_query = pda_metadata_query.format(str(source_schema_list).strip('[').strip(']'),str(source_table_list).strip('[').strip(']'))
        print(source_query)
        if source_db_driver == 'com.ibm.db2.jcc.DB2Driver':
            source_metadata = db_connect.exec_sql_with_jdbc(source_db_node, source_user, source_pwd, source_query)
        else:
            source_metadata = db_connect.exec_sql_common(source_db_node, source_user, source_pwd, source_query)

        '''table to map'''
        source_table_columns_dict = {}
        for item in source_metadata:
            source_table_columns = item['TABLE_SCHEMA'].strip() + "." + item['TABLE_NAME']
            column_dict = {}
            column_dict['COLUMN_NAME'] = item['COLUMN_NAME']
            column_dict['COLUMN_NUMBER'] = item['COLUMN_NUMBER']
            column_dict['COLUMN_TYPE'] = item['COLUMN_TYPE']
            column_dict['COLUMN_LENGTH'] = item['COLUMN_LENGTH']
            column_dict['KEY_SEQ'] = item['KEY_SEQ']
            if source_table_columns_dict.__contains__(source_table_columns):
                source_table_columns_dict[source_table_columns].append(column_dict)
            else:
                column_list = []
                column_list.append(column_dict)
                source_table_columns_dict[source_table_columns] = column_list
        print(source_table_columns_dict)
        '''Store the table mapping to a temp file'''
        file_name = os.path.join(conf.read_temp_dir(),'source_metadata.tmp')
        print(file_name)
        with open(file_name,'w') as f:
            json.dump(source_table_columns_dict,f)
        print("Step 4: Get target tables' column list.")
        '''get target tables' metadata'''
        target_db_driver = conf.Read_db_config(target_db_node)['driver']
        print('target db driver:'+target_db_driver)
        if target_db_driver == '{IBM DB2 ODBC DRIVER}' or target_db_driver == 'com.ibm.db2.jcc.DB2Driver':
            target_query = db2_metadata_query.format(str(target_schema_list).strip('[').strip(']'),str(target_table_list).strip('[').strip(']'))
            print(target_query)
        else:
            target_query = pda_metadata_query.format(str(target_schema_list).strip('[').strip(']'),str(target_table_list).strip('[').strip(']'))
        print(target_query)

        if target_db_driver == 'com.ibm.db2.jcc.DB2Driver':
            target_metadata = db_connect.exec_sql_with_jdbc(target_db_node, target_user, target_pwd, target_query)
        else:
            target_metadata = db_connect.exec_sql_common(target_db_node, target_user, target_pwd, target_query)

        '''table to map'''
        target_table_columns_dict = {}
        for item in target_metadata:
            target_table_columns = item['TABLE_SCHEMA'].strip() + "." + item['TABLE_NAME']
            column_dict = {}
            column_dict['COLUMN_NAME'] = item['COLUMN_NAME']
            column_dict['COLUMN_NUMBER'] = item['COLUMN_NUMBER']
            column_dict['COLUMN_TYPE'] = item['COLUMN_TYPE'].split('(')[0]
            column_dict['COLUMN_LENGTH'] = item['COLUMN_LENGTH']
            column_dict['KEY_SEQ'] = item['KEY_SEQ']
            if target_table_columns_dict.__contains__(target_table_columns):
                target_table_columns_dict[target_table_columns].append(column_dict)
            else:
                column_list = []
                column_list.append(column_dict)
                target_table_columns_dict[target_table_columns] = column_list
        print(target_table_columns_dict)


        '''Store the target metadata a temp file'''
        file_name = os.path.join(conf.read_temp_dir(),'target_metadata.tmp')
        print(file_name)
        with open(file_name,'w') as f:
            json.dump(target_table_columns_dict,f)

        '''Build source_target_column_mapping'''
        print("step 5: get source/target tables column mapping")
        source_target_column_mapping = []
        for item in source_target_table_mapping:
            source_table = item['SRC_OBJ_NM']
            target_table = item['TRGT_TBL_NM']
            source_columns = source_metadata[source_table]
            target_columns = target_metadata[target_table]
            for src_col in source_columns:
                for tar_col in target_columns:
                    if tar_col['COLUMN_NUMBER'] == src_col['COLUMN_NUMBER']:
                        source_target_column_mapping.append({"SOURCE_TABLE": source_table, "TARGET_TABLE": target_table,\
                                                             "SOURCE_COLUMN": src_col['COLUMN_NAME'],\
                                                             "TARGET_COLUMN": tar_col['COLUMN_NAME'],\
                                                             "SOURCE_COLUMN_NUMBER": src_col['COLUMN_NUMBER'],\
                                                             "TARGET_COLUMN_NUMBER": tar_col['COLUMN_NUMBER']})
        print(source_target_column_mapping)
        '''Store to temp'''
        file_name = os.path.join(conf.read_temp_dir(), 'source_target_column_mapping.tmp')
        print(file_name)
        with open(file_name, 'w') as f:
            json.dump(source_target_column_mapping, f)

        print("For each source table get source table sample data")




if __name__ == "__main__":

    conf = ReadConfig()
    sample_data = Sample_data_test()
    source_target_table_mapping = conf.read_source_target_table_mapping()
    print(source_target_table_mapping)
    source_metadata = json.load(open('../tmp/source_metadata.tmp','r'))
    print(source_metadata)
    target_metadata = json.load(open('../tmp/target_metadata.tmp','r'))
    print(target_metadata)
    source_target_column_mapping = json.load(open('../tmp/source_target_column_mapping.tmp', 'r'))

    
    for item in source_target_table_mapping:
        source_table = item['SRC_OBJ_NM']
        target_table = item['TRGT_TBL_NM']
        print(source_table)
        source_key = []
        source_column_list = []
        target_column_list = []
        source_where_condition = conf.Read_where_condition(source_table)
        for row in source_metadata[source_table]:
            source_column_list.append(row['COLUMN_NAME'])
            if row['KEY_SEQ'] != '0':
                source_key.append(row['COLUMN_NAME'])
        print('source_column_list:' + str(source_column_list))
        print('source_key:' + str(source_key))
        for row in target_metadata[target_table]:
            target_column_list.append(row['COLUMN_NAME'])
        print("Target_column_list:"+str(target_column_list))
        source_column_str = str(source_column_list).strip('[').strip(']').replace("'", '')
        target_column_str = str(target_column_list).strip('[').strip(']').replace("'", '')
        print('Source Column str:' + source_column_str)
        print('Target Column str:' + target_column_str)
        source_sample_query_run_flag = False
        target_sample_query_run_flat = False
        if source_where_condition != 'NULL':
            source_sample_query = "select" + source_column_str + " from " + \
                                 source_table + source_where_condition
            print(source_sample_query)
            target_where_condition = sample_data.source_condition_transfer(source_table,source_where_condition)
            target_sample_query = "select" + target_column_str + " from " +\
                target_table + target_where_condition
            print(source_sample_query)

        elif len(source_key)!= 0:
            #source_sample_query = "select RAND()*50 as RANDOM_KEY, " + source_column_str + " from " + source_table + " order by RANDOM_KEY fetch first 10 rows only"
            source_sample_query = "with a as (select RAND()*50 as RANDOM_KEY, {} from {} \
            order by RANDOM_KEY fetch first 10 rows only) select {} from a order by {} asc"\
                .format(source_column_list,source_table,source_column_list,str(source_key).strip('[').strip(']').replace("'",''))
            print(source_sample_query)
            '''connecting to source to get sample data'''
            source_db_driver = 'com.ibm.db2.jcc.DB2Driver'
            if source_db_driver == 'com.ibm.db2.jcc.DB2Driver':
                source_sample_data = db_connect.exec_sql_with_jdbc('siwdb2_jdbc', 'pdaetlg', 'jun10jun',
                                                                   source_sample_query)
            else:
                source_sample_data = db_connect.exec_sql_common('xx', 'xx', 'xx',
                                                                source_sample_query)
            print(source_sample_data)
            source_sample_query_run_flag = True
            target_condition_str = " where"
            target_key_list = []
            for item in source_key:
                target_key = ''
                primary_key_value_list = []
                for row in source_target_column_mapping:
                    if row['SOURCE_COLUMN'] == item and row['SOURCE_TABLE'] == source_table:
                        target_key = row['TARGET_COLUMN']
                        target_key_list.append(target_key)
                for row in source_sample_data:
                    primary_key_value_list.append(row[item])
                if item == source_key[-1]:
                    target_condition_str = target_condition_str + target_key+" in ({})".format(str(primary_key_value_list).strip('[').strip(']'))
                else:
                    target_condition_str = target_condition_str + target_key + " in ({}) and ".format(
                        str(primary_key_value_list).strip('[').strip(']'))
            target_condition_str += "order by {} asc".format(str(source_key).strip('[').strip(']').replace("'",''))
            print(str(target_condition_str))
            target_sample_query = "select {} from {} {}".format(target_column_str,target_table,target_condition_str)
            print(target_sample_query)
        else:
            source_sample_query = "select {} from {}".format(source_column_str,source_table)
            target_sample_query = "select {} from {}".format(target_column_str,target_table)

        if source_sample_query_run_flag == False:
            '''Run in source'''
            source_db_driver = 'com.ibm.db2.jcc.DB2Driver'
            if source_db_driver == 'com.ibm.db2.jcc.DB2Driver':
                source_sample_data = db_connect.exec_sql_with_jdbc('siwdb2_jdbc', 'pdaetlg', 'jun10jun',
                                                                   source_sample_query)
            else:
                source_sample_data = db_connect.exec_sql_common('xx', 'xx', 'xx',
                                                                source_sample_query)
            print(source_sample_data)
        if source_sample_query_run_flag == False:
            '''Run in Target'''
            target_db_driver = '{NetezzaSQL}'
            if target_db_driver == 'com.ibm.db2.jcc.DB2Driver':
                target_sample_data = db_connect.exec_sql_with_jdbc('xx', 'xx', 'xx',
                                                                   target_sample_query)
            else:
                target_sample_data = db_connect.exec_sql_common('siwodspda', 'siwsit', 'SIWJul2019JulSIW',
                                                                target_sample_query)
            print(target_sample_data)

        '''validation'''

    '''
    sample_data = Sample_data_test()
    sample_data.sample_data_test('siwdb2_jdbc','siwdsd','aug27aug','siwodspda','siwsit','SIWJul2019JulSIW')
    '''

















