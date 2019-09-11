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
        #print(source_condition_str)
        source_target_column_mapping = json.load(open('../tmp/source_target_column_mapping.tmp', 'r'))
        orderby_column_list = []
        if source_condition_str.find('order by') != -1:
            condition_str = source_condition_str.split('order by')[0]
            orderby_str = source_condition_str.split('order by')[1]
            condition_list = re.split(r'where|and',condition_str)
            #print("condition_list"+str(condition_list))
            if orderby_str.find(',') != -1:
                #print('exist')
                orderby_column_list = orderby_str.split(',')
            else:
                #print('not exist')
                orderby_column_list.append(orderby_str)
            orderby_column_list[-1] = orderby_column_list[-1].strip().split(' ')[0]
            #print("orderby_list:" + str(orderby_list))
        else:
            condition_list = re.split(r'where|and', source_condition_str)
        target_condition_str = source_condition_str
        source_column_list = []
        for item in condition_list:
            if item.strip() != '':
                source_column = item.split('=')[0].strip()
                source_column_list.append(source_column)
        for item in orderby_column_list:
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

    def Date_time_format_transfer(self,str):
        pattern = re.compile(
            r'(((([1-2]{1}[0-9]{3})\-[0-1]{1}[0-9]{1})\-[0-3]{1}[0-9]{1})\s[0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}:[0-5]{1}[0-9]{1})\.[0-9]{3,6}')
        #print(pattern.findall(str))
        out = re.sub(pattern, lambda x: x.group(1), str)
        return out
        #print(result)

    def Lookup_row(self,source_row,target_table_list,source_target_column_mapping):
        for item in target_table_list:
            compare_flag = False
            for k,v in source_target_column_mapping:
                if item[v] == source_row[k]:
                    compare_flag = True
                else:
                    compare_flag = False
                    break
        if compare_flag == False:
            return False
        else:
            return True





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
            source_columns = source_table_columns_dict[source_table]
            target_columns = target_table_columns_dict[target_table]
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

        '''For each source build key_value mapping of columns'''
        source_target_column_mapping_dict = {}
        one_table_src_tgt_col_mapping_dict = {}
        for items in source_target_column_mapping:
            if source_target_column_mapping_dict.__contains__(items['SOURCE_TABLE']):
                one_table_src_tgt_col_mapping_dict[items['SOURCE_COLUMN']] = items['TARGET_COLUMN']
                source_target_column_mapping_dict[items['SOURCE_TABLE']] = one_table_src_tgt_col_mapping_dict
            else:
                one_table_src_tgt_col_mapping_dict = {}
                one_table_src_tgt_col_mapping_dict[items['SOURCE_COLUMN']] = items['TARGET_COLUMN']
                source_target_column_mapping_dict[items['SOURCE_TABLE']] = one_table_src_tgt_col_mapping_dict
        print("source_target_column_mapping_dict" + str(source_target_column_mapping_dict))


        print("For each source table get source table sample data")
        for item in source_target_table_mapping:
            source_table = item['SRC_OBJ_NM']
            target_table = item['TRGT_TBL_NM']
            print("Source table name:"+source_table)
            source_key = []
            source_column_list = []
            target_column_list = []
            source_where_condition = conf.Read_where_condition(source_table)
            for row in source_table_columns_dict[source_table]:
                source_column_list.append(row['COLUMN_NAME'])
                if row['KEY_SEQ'] != '0':
                    source_key.append(row['COLUMN_NAME'])

            print('source_column_list:' + str(source_column_list))
            print('source_key:' + str(source_key))
            for row in target_table_columns_dict[target_table]:
                target_column_list.append(row['COLUMN_NAME'])
            print("Target_column_list:" + str(target_column_list))
            source_column_str = str(source_column_list).strip('[').strip(']').replace("'", '')
            target_column_str = str(target_column_list).strip('[').strip(']').replace("'", '')
            print('Source Column str:' + source_column_str)
            print('Target Column str:' + target_column_str)
            source_sample_query_run_flag = False
            target_sample_query_run_flag = False
            if source_where_condition != 'NULL':
                source_sample_query = "select {} from {} {}".format(source_column_str, source_table,
                                                                    source_where_condition)
                print("source_sample_query:" + source_sample_query)
                target_where_condition = self.source_condition_transfer(source_table, source_where_condition)
                target_sample_query = "select {} from {} {}".format(target_column_str, target_table,
                                                                    target_where_condition)
                print("target_sample_query" + target_sample_query)

            elif len(source_key) != 0:
                source_sample_query = "with a as (select RAND()*50 as RANDOM_KEY, {} from {} \
                order by RANDOM_KEY fetch first 10 rows only) select {} from a order by {} asc" \
                    .format(source_column_str, source_table, source_column_str,
                            str(source_key).strip('[').strip(']').replace("'", ''))
                print(source_sample_query)
                if source_db_driver == 'com.ibm.db2.jcc.DB2Driver':
                    source_sample_data = db_connect.exec_sql_with_jdbc('siwdb2_jdbc', 'pdaetlg', 'sep09sep',
                                                                       source_sample_query)
                else:
                    source_sample_data = db_connect.exec_sql_common('xx', 'xx', 'xx',
                                                                    source_sample_query)
                source_sample_query_run_flag = True

                '''format timestamp'''

                source_sample_data_formated = eval(self.Date_time_format_transfer(str(source_sample_data)))
                #print(type(source_sample_data_formated),type(source_sample_data_formated[0]),source_sample_data_formated)
                file_name = os.path.join(conf.read_temp_dir(), source_table + "_sample.tmp")
                with open(file_name, 'w') as f:
                    json.dump(source_sample_data_formated, f)

                target_condition_str = " where "
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
                        target_condition_str = target_condition_str + target_key + " in ({})".format(
                            str(primary_key_value_list).strip('[').strip(']'))
                    else:
                        target_condition_str = target_condition_str + target_key + " in ({}) and ".format(
                            str(primary_key_value_list).strip('[').strip(']'))
                target_condition_str += "order by {} asc".format(str(target_key).strip('[').strip(']').replace("'", ''))
                print(str(target_condition_str))
                target_sample_query = "select {} from {} {}".format(target_column_str, target_table,
                                                                    target_condition_str)
                print(target_sample_query)
            else:
                source_sample_query = "select {} from {}".format(source_column_str, source_table)
                target_sample_query = "select {} from {}".format(target_column_str, target_table)

            if source_sample_query_run_flag == False:
                print("Source table name:"+source_table)
                source_db_driver = 'com.ibm.db2.jcc.DB2Driver'
                if source_db_driver == 'com.ibm.db2.jcc.DB2Driver':
                    source_sample_data = db_connect.exec_sql_with_jdbc('siwdb2_jdbc', 'pdaetlg', 'sep09sep',
                                                                       source_sample_query)
                else:
                    source_sample_data = db_connect.exec_sql_common('xx', 'xx', 'xx',
                                                                    source_sample_query)
                '''format timestamp'''

                source_sample_data_formated = eval(self.Date_time_format_transfer(str(source_sample_data)))
                #print(type(json.loads(source_sample_data_formated)),json.loads(source_sample_data_formated))
                file_name = os.path.join(conf.read_temp_dir(), source_table + "_sample.tmp")
                with open(file_name, 'w') as f:
                    json.dump(source_sample_data_formated, f)

            if target_sample_query_run_flag == False:
                print("Target table name:" + target_table)
                if target_db_driver == 'com.ibm.db2.jcc.DB2Driver':
                    target_sample_data = db_connect.exec_sql_with_jdbc('xx', 'xx', 'xx',
                                                                       target_sample_query)
                else:
                    target_sample_data = db_connect.exec_sql_common('siwodspda', 'siwgit', 'SIWJul2019JulSIW',
                                                                    target_sample_query)
                print(target_sample_data)
                file_name = os.path.join(conf.read_temp_dir(), target_table + "_sample.tmp")
                with open(file_name, 'w') as f:
                    json.dump(target_sample_data, f)
                '''validation'''
                source_diff_list = []
                target_diff_list = []
                for source_row in source_sample_data_formated:
                    for target_row in target_sample_data:
                        compare_flag = False
                        for k, v in source_target_column_mapping_dict[source_table].items():
                            if target_row[v] == source_row[k]:
                                compare_flag = True
                            else:
                                compare_flag = False
                                break
                        if compare_flag == True:
                            break
                    if compare_flag == False:
                        source_diff_list.append(source_row)
                    else:
                        pass

                for target_row in target_sample_data:
                    for source_row in source_sample_data_formated:
                        compare_flag = False
                        for k, v in source_target_column_mapping_dict[source_table].items():
                            if source_row[k] == target_row[v]:
                                compare_flag = True
                            else:
                                compare_flag = False
                                break
                        if compare_flag == True:
                            break
                    if compare_flag == False:
                        target_diff_list.append(target_row)
                    else:
                        pass
                print("source_diff_list:" + str(source_diff_list))
                print("target_diff_list:" + str(target_diff_list))





if __name__ == "__main__":

    conf = ReadConfig()
    sample_data = Sample_data_test()
    sample_data.sample_data_test('siwdb2_jdbc', 'pdaetlg', 'sep09sep','siwodspda','siwgit','SIWJul2019JulSIW')


    
    #source_target_table_mapping = conf.read_source_target_table_mapping()
    #print(source_target_table_mapping)
    #source_metadata = json.load(open('../tmp/source_metadata.tmp','r'))
    #print(source_metadata)
    #target_metadata = json.load(open('../tmp/target_metadata.tmp','r'))
    #print(target_metadata)
    '''
    source_target_column_mapping = json.load(open('../tmp/source_target_column_mapping.tmp', 'r'))

    #str = "[{'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'BCP Elimination                                                                                     ', 'REV_COST_CAT_CD': 'C0110', 'REV_COST_MINOR_CD': '0110', 'UPDATED_AT_TS': '2007-04-02 06:44:39.696625', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'H/W Maintenance                                                                                     ', 'REV_COST_CAT_CD': 'C0133', 'REV_COST_MINOR_CD': '0133', 'UPDATED_AT_TS': '2007-04-02 06:44:39.696625', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'Rated Services                                                                                      ', 'REV_COST_CAT_CD': 'C0138', 'REV_COST_MINOR_CD': '0138', 'UPDATED_AT_TS': '2007-04-02 06:44:39.696625', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'Shared Infrastructure                                                                               ', 'REV_COST_CAT_CD': 'C0139', 'REV_COST_MINOR_CD': '0139', 'UPDATED_AT_TS': '2007-04-02 06:44:39.696625', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'Over/Under Allocation                                                                               ', 'REV_COST_CAT_CD': 'C0140', 'REV_COST_MINOR_CD': '0140', 'UPDATED_AT_TS': '2007-04-02 06:44:39.696625', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'Provisions                                                                                          ', 'REV_COST_CAT_CD': 'C0141', 'REV_COST_MINOR_CD': '0141', 'UPDATED_AT_TS': '2007-04-02 06:44:39.696625', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'Transition Amortization                                                                             ', 'REV_COST_CAT_CD': 'C0144', 'REV_COST_MINOR_CD': '0144', 'UPDATED_AT_TS': '2011-04-13 20:29:35.555406', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'NON-OPERATING ACQUISITION RELATED CHARGES                                                           ', 'REV_COST_CAT_CD': 'C0294', 'REV_COST_MINOR_CD': '0294', 'UPDATED_AT_TS': '2011-01-10 16:32:50.29779', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'Non-Operating Activity for Pension                                                                  ', 'REV_COST_CAT_CD': 'C0297', 'REV_COST_MINOR_CD': '0297', 'UPDATED_AT_TS': '2011-01-10 16:38:20.614118', 'UPDATED_BY_CNUM': '          '}, {'REV_COST_TYP_CD': 'C', 'STATUS': 'O', 'REV_COST_CAT_DESC': 'Expense Recovery Cost                                                                               ', 'REV_COST_CAT_CD': 'C0600', 'REV_COST_MINOR_CD': '0600', 'UPDATED_AT_TS': '2007-04-02 06:44:39.696625', 'UPDATED_BY_CNUM': '          '}]"
    #result = sample_data.Date_time_format_transfer(str)
    #print(result)

    source_target_column_mapping_dict = {}
    one_table_src_tgt_col_mapping_dict = {}
    for items in source_target_column_mapping:
        if source_target_column_mapping_dict.__contains__(items['SOURCE_TABLE']):
            one_table_src_tgt_col_mapping_dict[items['SOURCE_COLUMN']] = items['TARGET_COLUMN']
            source_target_column_mapping_dict[items['SOURCE_TABLE']] = one_table_src_tgt_col_mapping_dict
        else:
            one_table_src_tgt_col_mapping_dict = {}
            one_table_src_tgt_col_mapping_dict[items['SOURCE_COLUMN']] = items['TARGET_COLUMN']
            source_target_column_mapping_dict[items['SOURCE_TABLE']] = one_table_src_tgt_col_mapping_dict
    print("source_target_column_mapping_dict" + str(source_target_column_mapping_dict))



    source_sample_data_formated = json.load(open('../tmp/BMSIW.REV_COST_CAT_REF_sample.tmp','r'))
    print("source_sample_data_formated"+str(type(source_sample_data_formated)),source_sample_data_formated)

    target_sample_data = json.load(open('../tmp/CNTRCTFI.REVENUE_COST_CATEGORY_REFERENCE_sample.tmp','r'))
    source_table = 'BMSIW.REV_COST_CAT_REF'
    target_table = 'CNTRCTFI.REVENUE_COST_CATEGORY_REFERENCE'
    print("target_sample_data"+str(target_sample_data))

    
    source_diff_list = []
    target_diff_list = []
    for source_row in source_sample_data_formated:
        print(source_row)
        for target_row in target_sample_data:
            compare_flag = False
            print("target row:" + str(target_row))
            for k, v in source_target_column_mapping_dict[source_table].items():
                print(k)
                print(v)
                if target_row[v] == source_row[k]:
                    compare_flag = True
                else:
                    compare_flag = False
                    break
                print(compare_flag)
            if  compare_flag == True:
                break
        if compare_flag == False:
            source_diff_list.append(source_row)
        else:
            pass

    for target_row in target_sample_data:
        for source_row in source_sample_data_formated:
            compare_flag = False
            for k, v in source_target_column_mapping_dict[source_table].items():
                if source_row[k] == target_row[v]:
                    compare_flag = True
                else:
                    compare_flag = False
                    break
            if  compare_flag == True:
                break
        if compare_flag == False:
            target_diff_list.append(target_row)
        else:
            pass
    print("source_diff_list:" + str(source_diff_list))
    print("target_diff_list:" + str(target_diff_list))
    '''
    



































