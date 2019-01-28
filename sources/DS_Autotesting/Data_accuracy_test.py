# -*- coding: utf-8 -*-
from Read_conf import ReadConfig
import TestException
import datetime
import db_connect
import json

class Data_accuracy_test:

    def get_case_description(testcase):
        '''decorate function'''

        def decorator(test_case_func):
            def inner(*args, **kwargs):
                if testcase == 'Rowcount':
                    print('Rowcount test case started at:%s' % datetime.datetime.now())
                    return test_case_func(*args, **kwargs)

            return (inner)
        return (decorator)


    def generate_source_target_column_map(self,id,pwd,source_schema,source_table,target_schema,target_table):
        db2_column_sample_sql = '''
        SELECT NAME as COL_NM,COLNO as COL_NO
        FROM SYSIBM.SYSCOLUMNS
        WHERE UPPER(TBNAME) IN (SELECT UPPER(NAME) FROM SYSIBM.SYSTABLES WHERE TYPE = 'T') AND
        UPPER(TBCREATOR) = UPPER('{}') -- Schema Name
        AND UPPER (TBNAME) = UPPER('{}') ORDER BY COLNO
        '''
        pda_column_sample_sql = """
        SELECT  ATTNAME as COL_NM,ATTNUM as COL_NO
        FROM _V_RELATION_COLUMN 
        WHERE UPPER(TYPE) = 'TABLE' AND 
        UPPER(SCHEMA) = UPPER('BDWDB') -- Schema Name
        AND UPPER(NAME) = UPPER('{}') ORDER BY ATTNUM;
        """
        print(db2_column_sample_sql)
        print(pda_column_sample_sql)

        '''read source data dic'''

        conf = ReadConfig()
        source_db_node = conf.Read_source_db_node()
        target_db_node = conf.Read_target_db_node()
        source_db = conf.Read_db_config(source_db_node)
        target_db = conf.Read_db_config(target_db_node)
        if source_db['db_type'] == 'db2':
            source_db_sql = db2_column_sample_sql.format(source_schema,source_db)
        elif source_db['db_type'] == 'pda':
            source_db_sql = db2_column_sample_sql.format(source_schema,source_db)
        else:
            source_db_sql = None
            print("The db type is valid")

        if target_db['db_type'] == 'db2':
            target_db_sql = db2_column_sample_sql.format(source_schema,source_db)
        elif target_db['db_type'] == 'pda':
            target_db_sql = db2_column_sample_sql.format(source_schema,source_db)
        else:
            target_db_sql = None
            print("The db type is valid")
        ''' run under source to get source columns'''
        print(source_db_sql)
        print(target_db_sql)
        source_target_mapping = dict()
        rs_source = db_connect.exec_sql_common(source_db_node, id, pwd, source_db_sql)
        rs_target = db_connect.exec_sql_common(target_db_node, id, pwd, target_db_sql)

        for src_line in rs_source:
            source_column_nm = src_line['COL_NM']
            source_column_no = src_line['COL_NO']
            for tgt_line in rs_target:
                if tgt_line['COL_NO'] == source_column_no:
                    source_target_mapping[source_column_nm] = tgt_line['COL_NM']
        return source_target_mapping


    @get_case_description("Rowcount")
    def rowcount_test(self, source_id, source_pwd, target_id,target_pwd):
        '''read config file for the table list'''
        conf = ReadConfig()
        table_list = conf.Read_table_list()
        '''define source db,target db'''
        source_db_node = conf.Read_source_db_node()
        target_db_node = conf.Read_target_db_node()
        rowcount_report = []
        fail_count = 0
        for table in table_list:
            rowcount_result = dict()
            source_table = table['SOURCE_SCHEMA'] + '.' + table['SOURCE_TABLE']
            target_table = table['TARGET_SCHEMA'] + '.' + table['TARGET_TABLE']
            source_sql = 'select count(*) as rowcount from {}'.format(source_table)
            target_sql = 'select count(*) as rowcount from {}'.format(target_table)
            '''connect to source and target DB to run the sql'''
            '''run sql in target first'''
            rs_source = db_connect.exec_sql_common(source_db_node, source_id, source_pwd, source_sql)
            source_rowcount = rs_source[0].rowcount
            rs_target = db_connect.exec_sql_common(target_db_node, target_id, target_pwd, target_sql)
            target_rowcount = rs_target[0].rowcount
            if source_rowcount == target_rowcount:
                status = 'PASS'
            else:
                status = 'FAIL'
                fail_count += 1

            rowcount_result['SOURCE_TABLE'] = source_table
            rowcount_result['TARGET_TABLE'] = target_table
            rowcount_result['SOURCE_ROWCOUNT'] = source_rowcount
            rowcount_result['TARGET_ROWCOUNT'] = target_rowcount
            rowcount_result['STATUS'] = status
            rowcount_report.append(rowcount_result)
        with open("tmp/rowcountreport.csv", "w") as f:
            f.write(str(rowcount_report))

        if fail_count > 0:
            print("The rowcount test passed,detail see the rowcount report")

        else:
            print("The rowcount test failed,detail see the rowcount report")
            raise TestException.RowcountError()


    @get_case_description("SampleData")
    def sample_data_test(self, id, pwd):
        '''read conf'''
        conf = ReadConfig()
        table_list = conf.Read_table_list()
        source_db_node = conf.Read_source_db_node()
        target_db_node = conf.Read_target_db_node()
        sample_data_report = []
        failed_sample_report = []
        fail_cell_count = 0
        for table in table_list:
            '''get the source target column mapping'''
            source_target_column_mapping = self.generate_source_target_column_map(id, pwd,table['SOURCE_SCHEMA'],\
                table['SOURCE_TABLE'], table['TARGET_SCHEMA'], table['TARGET_TABLE'])
            source_table_nm = table['SOURCE_SCHEMA']+'.'+table['SOURCE_TABLE']
            target_table_nm = table['TARGET_SCHEMA'] + '.' + table['TARGET_TABLE']
            sample_source_condition = conf.Read_where_condition(table['SOURCE_TABLE'])
            sample_target_condition = conf.Read_where_condition(table['TARGET_TABLE'])
            source_sql = "select * from {} where {}".format(source_table_nm,sample_source_condition)
            target_sql = "select * from {} where {}".format(target_table_nm,sample_target_condition)
            rs_source = db_connect.exec_sql_common(source_db_node, id, pwd, source_sql)
            rs_target = db_connect.exec_sql_common(target_db_node, id, pwd, target_sql)
            source_row_count = len(rs_source)
            target_row_count = len(rs_target)
            source_column_count = len(rs_source[0])
            target_column_count = len(rs_target[0])
            print("source table: %s" % source_table_nm)
            print("target table: %s" % target_table_nm)

            '''step 1 compare the row number between source and target'''
            if source_row_count == target_row_count:
                print("The sample sql returns the same row count")
            else:
                print("The sample sql returns the different row count,the test validate failed")
                raise TestException.SampleDataError
                '''step 2 compare the column number between source and target'''
            if source_column_count == target_column_count + 3:
                print("The sample sql return the same column count")
            else:
                print("The sample sql returns the different row count,the test validate failed")
                raise TestException.SampleDataError

                '''step 3 loop to compare the result from source and target'''

                for i in range(source_row_count):
                    for k, v in source_target_column_mapping.items():
                        sample_compare_dict = dict()
                        source_value = rs_source[i][k]
                        target_value = rs_target[i][v]
                        sample_compare_dict['SOURCE_TABLE_NM'] = source_table_nm
                        sample_compare_dict['SOURCE_COLUMN_NM'] = k
                        sample_compare_dict['SOURCE_COLUMN_VALUE'] = source_value
                        sample_compare_dict['TARGET_TABLE_NM'] = target_table_nm
                        sample_compare_dict['TARGET_COLUMN_NM'] = v
                        sample_compare_dict['TARGET_COLUMN_VALUE'] = target_value
                        sample_compare_dict['STATUS'] = ('PASS' if(source_value == target_value) else 'FAIL')
                        sample_data_report.append(sample_compare_dict)
                        if sample_compare_dict['STATUS'] == 'FAIL':
                            failed_sample_report.append[sample_compare_dict]
        '''write failed record to failed file '''
        with open("tmp/failed_sample_data_report.json",'w',encoding ='UTF-8') as f:
            json.dump(failed_sample_report, f)
        '''write all the record to report file'''
        with open("tmp/sample_data_report.json",'w',encoding ='UTF-8') as f:
            json.dump(sample_data_report, f)

        if len(failed_sample_report) > 0:
            print("There are some cell values not equal, the test failed,check the failed report file for detail")
            raise TestException.SampleDataError()
        else:
            print("The sample data test run passed")
        return 'PASS'

if __name__ == "__main__":
    acc_test = Data_accuracy_test()
    acc_test.generate_source_target_column_map('','','','')
