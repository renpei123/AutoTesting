# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 16:30:03 2019

@author: RongHe
"""

# -*- coding: utf-8 -*-
import DS_Operation
from Read_conf import ReadConfig
import TestException
import sys
import datetime
import db_connect

class ASCA_test:

    MonthEnum = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}    
    def job_status_time_transfer(self,date_time_string):
        str = "Wed Jan 16 09:58:58 2019"
        date_format = str.split(' ')
        year = int(date_format[4])
        month = self.MonthEnum[date_format[1]]
        day = int(date_format[2])
        hour = int(date_format[3].split(':')[0])
        minute = int(date_format[3].split(':')[1])
        second = int(date_format[3].split(':')[2])
        run_time = datetime.datetime(year,month,day,hour,minute,second)
        print(run_time) 
        
    
    
    
    def get_case_description(testcase):
        '''decorate function'''    
        def decorator(test_case_func):
            def inner(*args,**kwargs):
                if testcase == 'ASCA':
                    print('ASCA test case started at:%s' % datetime.datetime.now() )
                    return test_case_func(*args,**kwargs)
                elif  testcase == 'jobStreamNegative':
                    print('IWRefresh test case started at: %s',datetime.datetime.now() )
                    return test_case_func(*args,**kwargs)
            return(inner)
        return(decorator)

        
        
        
        
        
    
    @get_case_description("ASCA")
    def asca_test(self,job_name):
        '''read config file for the job stream'''
        conf = ReadConfig()
        job_list = conf.Read_job_list()
        job_status_report = conf.job_status_report_file()
        for job in job_list:
            if job['JOB_ID'] != '':
                job_name = job['JOB_NAME']
                job_run_status = job_status_report[job_name]['Job Status']
                job_last_run_time = job_status_time_transfer(job_status_report[job_name]['Last Run Time'])
                #####step 1 validate if the parallel job show pass
                if job_run_status == 'Run OK(1)' or job_run_status == 'Run OK(1)':
                    print("step one validate the parallel job status is ok...")
                else :
                    print("The parallel status is failed")
                    raise TestException.ASCAControlError()
                #####step 2 validate if the ASCA Control record shows pass and the ASCA CONTORL TMS is after the job last run time"
                ''' get the bludb conf'''
                db_node = 'bluedb2'
                sql = "select * from ASCA.ASCA_CONTROL_RECORD WHERE JOB_ID = %s where ASCA_CNTL_TMS = MAX(ASCA_CNTL_TMS)" %job['JOB_ID']
                print(sql)
                db_connect.exec_sql_db2(db_node,'siwwebd','Bluemix_jan18jan','select * from XLSSTG.LOAD_APPLICATION')
                
                                
                
                
                
            
        
        
        job_run_result = job_status_report[job_name]
        job_status=job_run_result['Job Status']
        job_last_run_time = self.job_status_time_transfer(job_run_result['Last Run Time'])
        
            
if __name__ == "__main__":
    asca = ASCA_test()
    runtime = asca.job_status_time_transfer('Wed Jan 16 09:58:58 2019')
                
                
            
            
        
        
        



