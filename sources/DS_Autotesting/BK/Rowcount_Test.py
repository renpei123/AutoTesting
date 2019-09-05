# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 16:30:03 2019

@author: RongHe
"""

from Common.Read_conf import ReadConfig
import datetime
from Common import db_connect, TestException


class Rowcount_test:
    MonthEnum = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                 'Nov': 11, 'Dec': 12}


    def get_case_description(testcase):
        '''decorate function'''

        def decorator(test_case_func):
            def inner(*args, **kwargs):
                if testcase == 'Rowcount':
                    print('Rowcount test case started at:%s' % datetime.datetime.now())
                    return test_case_func(*args, **kwargs)
                elif testcase == 'jobStreamNegative':
                    print('Rowcount test case started at: %s', datetime.datetime.now())
                    return test_case_func(*args, **kwargs)

            return (inner)

        return (decorator)

    @get_case_description("IWRefresh")
    def rowcount_test(self,id,pwd):
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
            source_table = table['SOURCE_SCHEMA']+'.'+table['SOURCE_TABLE']
            target_table = table['TARGET_SCHEMA']+'.'+table['TARGET_TABLE']
            source_sql = 'select count(*) as rowcount from %s' % source_table
            target_sql = 'select count(*) as rowcount from %s' % target_table
            '''connect to source and target DB to run the sql'''
            '''run sql in target first'''
            rs_source = db_connect.exec_sql_common(source_db_node, id, pwd, source_sql)
            source_rowcount = rs_source[0].rowcount
            rs_target = db_connect.exec_sql_common(target_db_node, id, pwd, target_sql)
            target_rowcount = rs_target[0].rowcount
            status = ''
            if source_rowcount == target_rowcount:
                status = 'PASS'
            else:
                status = 'FAIL'
                fail_count += 1

            rowcount_result['SOURCE_TABLE']= source_table
            rowcount_result['TARGET_TABLE']= target_table
            rowcount_result['SOURCE_ROWCOUNT']= source_rowcount
            rowcount_result['TARGET_ROWCOUNT']= target_rowcount
            rowcount_result['TARGET_ROWCOUNT'] = target_rowcount
            rowcount_report.append(rowcount_result)
        with open("tmp/rowcountreport.csv","w") as f:
            f.write(str(rowcount_report))

        if fail_count > 0:
            print("The rowcount test passed,detail see the rowcount report")

        else:
            print("The rowcount test failed,detail see the rowcount report")
            raise TestException.RowcountError()

if __name__ == "__main__":
    rowcounttest = Rowcount_test()
    rowcounttest.rowcount_test()










