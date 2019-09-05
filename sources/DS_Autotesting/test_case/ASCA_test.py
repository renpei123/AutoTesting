# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 16:30:03 2019

@author: RongHe
"""

# -*- coding: utf-8 -*-
from Common.Read_conf import ReadConfig
import datetime
from Common import db_connect, TestException
from Common.generate_report import Generate_report

class ASCA_test:

    MonthEnum = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}    
    def job_status_time_transfer(self,date_time_string):
        str = date_time_string
        date_format = str.split(' ')
        year = int(date_format[4])
        month = self.MonthEnum[date_format[1]]
        day = int(date_format[2])
        hour = int(date_format[3].split(':')[0])
        minute = int(date_format[3].split(':')[1])
        second = int(date_format[3].split(':')[2])
        run_time = datetime.datetime(year,month,day,hour,minute,second)
        #print(run_time)
        return run_time

    def get_case_description(testcase):
        '''decorate function'''    
        def decorator(test_case_func):
            def inner(*args,**kwargs):
                if testcase == 'ASCA':
                    rc = ReadConfig()
                    print('ASCA test case started at:%s' % datetime.datetime.now())
                    with open(rc.read_asca_test_description(),'r',encoding='utf-8') as f:
                        description = f.read()
                    print(description)
                    return test_case_func(*args, **kwargs)
            return(inner)
        return(decorator)

    @get_case_description("ASCA")
    def asca_test(self,asca_db_node,zos_user,zos_pwd):
        '''read config file for the job stream'''
        conf = ReadConfig()
        job_list = conf.Read_job_list()
        job_status_report = conf.Read_job_status_report()
        asca_control_test_report =[]
        '''Get asca_control_record through jdbc, store the result to the asca_control_dict'''
        '''1. get the asca control id list'''
        asca_control_id_list =[]
        for job in job_list:
            if job['ASCA_CONTROL_POINT_ID'] != '':
                asca_control_id_list.append(job['ASCA_CONTROL_POINT_ID'])
        asca_control_id_string = str(asca_control_id_list).strip('[').strip(']')

        '''2.generate the sql query'''
        print("Step 1: Get asca control result from ASCA.ASCA_CNTROL_RECORD table")
        query = "select JOB_ID,ASCA_CNTL_PT_ID,SRC_ROW_CNT,TRGT_ROW_CNT,\
        SRC_CNTL_AMT,TRGT_CNTL_AMT,ASCA_CNTL_REC_ID,CNTL_STAT,\
        ASCA_CNTL_RUN_DT,ASCA_CNTL_TMS from(\
        SELECT RANK() OVER(PARTITION BY ASCA_CNTL_PT_ID ORDER BY ASCA_CNTL_TMS DESC)\
        AS RANK_NUM,JOB_ID,ASCA_CNTL_PT_ID,SRC_ROW_CNT,TRGT_ROW_CNT,\
        SRC_CNTL_AMT,TRGT_CNTL_AMT,ASCA_CNTL_REC_ID,CNTL_STAT,\
        ASCA_CNTL_RUN_DT,ASCA_CNTL_TMS from ASCA.ASCA_CONTROL_RECORD) AA WHERE AA.RANK_NUM=1\
        and AA.ASCA_CNTL_PT_ID in({})".format(asca_control_id_string)
        print("\tQuery:"+query)

        '''3. Trigger jdbc driver to query the data'''
        asca_control_result = db_connect.exec_sql_with_jdbc(asca_db_node, zos_user, zos_pwd, query)
        #print(asca_control_result)
        print("\tQuery running completed")
        print("Step 2:  start the validation the asca control result...")

        '''For each job, link the job name with the asca_control_result,perform validation and generate the report'''
        for job in job_list:
            if job['ASCA_CONTROL_POINT_ID'] != '':
                job_name = job['JOB_NAME']
                job_asca_cntl_pt_id =job['ASCA_CONTROL_POINT_ID']
                job_run_status = job_status_report[job_name]['Job Status']
                job_last_run_time = self.job_status_time_transfer(job_status_report[job_name]['Last Run Time'])
                print("\tValidated Job Name:"+job_name)
                '''step 1 validate if the parallel job show Complete'''
                if job_run_status == 'RUN OK (1)' or job_run_status == 'RUN OK (1)':
                    print("\t\tJob Status:" + job_run_status)
                else :
                    print("Job Status:" + job_run_status)
                    print("The parallel status validate date is failed,the test case not pass")
                    raise TestException.ASCAControlError()
                '''step 2 validate if the ASCA Control record shows pass and the ASCA CONTORL TMS is after the job last run time'''
                ''' get the asca control result from jdbc_query,with the same asca_control_pt_id'''
                exist_flag = False
                for asca_control_record in asca_control_result:
                    if asca_control_record['ASCA_CNTL_PT_ID'] == job_asca_cntl_pt_id:
                        #print(asca_control_record['ASCA_CNTL_PT_ID']+"vs"+job_asca_cntl_pt_id )
                        asca_control_test_report_row = dict()
                        exist_flag = True
                        asca_control_tms = datetime.datetime.strptime(asca_control_record['ASCA_CNTL_TMS'][0:19], "%Y-%m-%d %H:%M:%S")
                        if asca_control_tms > job_last_run_time:
                            asca_control_test_report_row['ASCA_CNTL_PT_ID'] = job_asca_cntl_pt_id
                            asca_control_test_report_row['JOB_NAME'] = job_name
                            asca_control_test_report_row['JOB_STATUS'] = job_run_status
                            asca_control_test_report_row['JOB_LAST_RUN_TIME'] = str(job_last_run_time)
                            asca_control_test_report_row['SOURCE_ROW_COUNT'] = asca_control_record['SRC_ROW_CNT']
                            asca_control_test_report_row['TARGET_ROW_COUNT'] = asca_control_record['TRGT_ROW_CNT']
                            asca_control_test_report_row['ASCA_CONTROL_STATUS'] = asca_control_record['CNTL_STAT']
                            asca_control_test_report_row['ASCA_CONTROL_TMS'] = asca_control_record['ASCA_CNTL_TMS']
                            asca_control_test_report_row['ASCA_TEST_RESULT'] = asca_control_record['CNTL_STAT']
                        else:
                            asca_control_test_report_row['ASCA_CNTL_PT_ID'] = job_asca_cntl_pt_id
                            asca_control_test_report_row['JOB_NAME'] = job_name
                            asca_control_test_report_row['JOB_STATUS'] = job_run_status
                            asca_control_test_report_row['JOB_LAST_RUN_TIME'] = str(job_last_run_time)
                            asca_control_test_report_row['SOURCE_ROW_COUNT'] = 'NULL'
                            asca_control_test_report_row['TARGET_ROW_COUNT'] = 'NULL'
                            asca_control_test_report_row['ASCA_CONTROL_STATUS'] = 'NULL'
                            asca_control_test_report_row['ASCA_CONTROL_TMS'] = 'NULL'
                            asca_control_test_report_row['ASCA_TEST_RESULT'] = 'FAIL'
                        asca_control_test_report.append(asca_control_test_report_row)
                        print("\t\tASCA_CONTROL_POINT_ID:" + asca_control_test_report_row['ASCA_CNTL_PT_ID'])
                        print("\t\tSOURCE_TABLE_ROW_COUNT:" + asca_control_test_report_row['SOURCE_ROW_COUNT'])
                        print("\t\tTARGET_TABLE_ROW_COUNT" + asca_control_test_report_row['TARGET_ROW_COUNT'])
                        print("\t\tRow Count Validate result:" + asca_control_test_report_row['ASCA_TEST_RESULT'])
                    #print("When the control id is"+job_asca_cntl_pt_id+ "asca_control_test_report"+str(asca_control_test_report))
                if exist_flag == False:
                    asca_control_test_report_row = dict()
                    asca_control_test_report_row['ASCA_CNTL_PT_ID'] = job_asca_cntl_pt_id
                    asca_control_test_report_row['JOB_NAME'] = job_name
                    asca_control_test_report_row['JOB_STATUS'] = job_run_status
                    asca_control_test_report_row['JOB_LAST_RUN_TIME'] = str(job_last_run_time)
                    asca_control_test_report_row['SOURCE_ROW_COUNT'] = 'NULL'
                    asca_control_test_report_row['TARGET_ROW_COUNT'] = 'NULL'
                    asca_control_test_report_row['ASCA_CONTROL_STATUS'] = 'NULL'
                    asca_control_test_report_row['ASCA_CONTROL_TMS'] = 'NULL'
                    asca_control_test_report_row['ASCA_TEST_RESULT'] = 'FAIL'
                    asca_control_test_report.append(asca_control_test_report_row)
                    print("\t\tASCA_CONTROL_POINT_ID:" + asca_control_test_report_row['ASCA_CNTL_PT_ID'])
                    print("\t\tSOURCE_TABLE_ROW_COUNT:" + asca_control_test_report_row['SOURCE_ROW_COUNT'])
                    print("\t\tTARGET_TABLE_ROW_COUNT" + asca_control_test_report_row['TARGET_ROW_COUNT'])
                    print("\t\tRow Count Validate result:" + asca_control_test_report_row['ASCA_TEST_RESULT'])
        ####################After all the records inserted to the asca_control_test_report
        '''Write dict to json file, then generate the xls report file through json file'''
        #print(asca_control_test_report)
        gen_asca = Generate_report()
        gen_asca.write_asca_status_to_json(asca_control_test_report)
        gen_asca.generate_asca_control_test_report()

        '''validate the test case result'''
        failed_count=0
        for item in asca_control_test_report:
            if item['ASCA_TEST_RESULT'] == 'FAIL':
                failed_count += 1
        if  failed_count > 0:
            print("One or more jobs' asca control not got pass, "
                  "check the asca_control_test_report.xls for detail")
            raise TestException.ASCAControlError()
        else:
            print("All jobs' asca control result got pass, ASCA Control test passed.")

            
if __name__ == "__main__":
    asca = ASCA_test()
    Str = "Thu Aug 22 14:54:10 2019"
    time_f = asca.job_status_time_transfer(Str)
    print(time_f)
                
                
            
            
        
        
        



