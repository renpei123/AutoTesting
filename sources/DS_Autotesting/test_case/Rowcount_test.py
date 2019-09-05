# -*- coding: utf-8 -*-
from Common.Read_conf import ReadConfig
import datetime
from Common import db_connect, TestException
from Common.generate_report import Generate_report
import os
import json

class Rowcount_test:

    def get_case_description(testcase):
        '''decorate function'''

        def decorator(test_case_func):
            def inner(*args, **kwargs):
                if testcase == 'Rowcount':
                    rc = ReadConfig()
                    print('Rowcount test case started at:%s' % datetime.datetime.now())
                    with open(rc.read_row_count_test_description(),'r',encoding='utf-8') as f:
                        description = f.read()
                    print(description)
                    return test_case_func(*args, **kwargs)
            return (inner)
        return (decorator)

    @get_case_description('Rowcount')
    def rowcount_test(asca_db_node, zos_user, zos_pwd):
        '''Step 1 get source/target table list from asca.asca_control_record'''
        conf = ReadConfig()
        job_list = conf.Read_job_list()
        '''Get asca_control_record through jdbc, store the result to the asca_control_dict'''
        '''1. get the asca control id list'''
        asca_control_id_list =[]
        for job in job_list:
            if job['ASCA_CONTROL_POINT_ID'] != '':
                asca_control_id_list.append(job['ASCA_CONTROL_POINT_ID'])
        asca_control_id_string = str(asca_control_id_list).strip('[').strip(']')

        '''2.generate the sql query'''
        print("Step 1: Get asca control result from ASCA.ASCA_CNTROL_RECORD table")
        query = "select SRC_OBJ_NM,TRGT_TBL_NM from ASCA.ASCA_control_point\
                WHERE ASCA_CNTL_PT_ID in ({})".format(asca_control_id_string)
        print("\tQuery:"+query)

        '''3. Trigger jdbc driver to query the data'''
        source_target_mapping = db_connect.exec_sql_with_jdbc(asca_db_node, zos_user, zos_pwd, query)
        '''Store the table mapping to a temp file'''
        file_name = os.path.join(conf.read_temp_dir(),'source_target_mapping.tmp')
        print(file_name)
        with open(file_name,'w') as f:
            json.dump(source_target_mapping,f)

        print(source_target_mapping)
        print("\tQuery running completed")
        print("Step 2:  start the get source table row count...")
        '''generate query'''
        source_db_node = conf.Read_source_db_node()
        query_str = ''
        for i in range(len(source_target_mapping)):
            if i < len(source_target_mapping)-1:
                query_str += "select '"+source_target_mapping[i]['SRC_OBJ_NM']+"' as TABLE_NM, count(*) as ROWCOUNT from "+source_target_mapping[i]['SRC_OBJ_NM'] + " union "
            else:
                query_str += "select '"+source_target_mapping[i]['SRC_OBJ_NM']+"' as TABLE_NM, count(*) as ROWCOUNT from "+source_target_mapping[i]['SRC_OBJ_NM']
        print(query_str)

        '''run the query '''
        source_rowcount = db_connect.exec_sql_with_jdbc(source_db_node, zos_user, zos_pwd, query_str)
        print(source_rowcount)

        print("Step 3: start get target table row count...")
        '''generate target query'''
        target_query = ''
        for i in range(len(source_target_mapping)):
            if i < len(source_target_mapping)-1:
                target_query += "select '"+source_target_mapping[i]['TRGT_TBL_NM']+"' as TABLE_NM, count(*) as ROWCOUNT from "+source_target_mapping[i]['TRGT_TBL_NM'] + " union "
            else:
                target_query += "select '"+source_target_mapping[i]['TRGT_TBL_NM']+"' as TABLE_NM, count(*) as ROWCOUNT from "+source_target_mapping[i]['TRGT_TBL_NM']
        print(target_query)
        '''get target db node'''
        target_db_node = conf.Read_target_db_node()
        db_conf = conf.Read_db_config(target_db_node)
        db_driver = db_conf['driver']
        print(db_driver)
        if db_driver == 'com.ibm.db2.jcc.DB2Driver':
            '''use jdbc to run query'''
            target_rowcount = db_connect.exec_sql_with_jdbc(target_db_node, zos_user, zos_pwd, target_query)
        else:
            '''use common driver to run query'''
            target_rowcount = db_connect.exec_sql_common(target_db_node,'siwsit','SIWJul2019JulSIW',target_query)
        print(target_rowcount)

        '''Step 4: validation'''
        print("Step 4: validation")
        Rowcount_test_result = []
        for item in source_target_mapping:
            rowcount_record = {}
            rowcount_record['SOURCE_TABLE'] = item['SRC_OBJ_NM']
            rowcount_record['TARGET_TABLE'] = item['TRGT_TBL_NM']
            for element in source_rowcount:
                if element['TABLE_NM'] == item['SRC_OBJ_NM']:
                    rowcount_record['SOURCE_ROWCOUNT'] = str(element['ROWCOUNT'])
            for element in target_rowcount:
                if element['TABLE_NM'] == item['TRGT_TBL_NM']:
                    rowcount_record['TARGET_ROWCOUNT'] = str(element['ROWCOUNT'])
            rowcount_record['TEST_RESULT'] = "PASS" if (rowcount_record['SOURCE_ROWCOUNT'] == rowcount_record['TARGET_ROWCOUNT']) else "FAIL"
            print("Source table name:"+rowcount_record['SOURCE_TABLE'])
            print("Target table name:" + rowcount_record['TARGET_TABLE'])
            print("Source table rowcount:"+rowcount_record['SOURCE_ROWCOUNT'] )
            print("Target table rowcount:"+rowcount_record['TARGET_ROWCOUNT'])
            print("Row count test result:"+rowcount_record['TEST_RESULT'])
            Rowcount_test_result.append(rowcount_record)
        print(Rowcount_test_result)

        '''generate report'''
        gen_rowcount = Generate_report()
        gen_rowcount.write_row_count_status_to_json(Rowcount_test_result)
        gen_rowcount.generate_row_count_test_report()

        '''validate the test case result'''
        failed_count=0
        for item in Rowcount_test_result:
            if item['TEST_RESULT'] == 'FAIL':
                failed_count += 1
        if failed_count > 0:
            print("One or more tables' rowcount between source and target mismatch, row count test failed "
                  "check the row_count_test_report.xls for detail")
            raise TestException.RowcountError()
        else:
            print("All tables' row count between source and target matched,the row count test passed.")













