# -*- coding: utf-8 -*-
import DS_Operation
import Read_conf
import TestException
import sys
import datetime


class Job_stream_test:
    
    def get_case_description(testcase):
        '''decorate function'''    
        def decorator(test_case_func):
            def inner(*args,**kwargs):
                if testcase == 'jobStreamPositive':
                    print('Job Stream test case started at:%s' % datetime.datetime.now() )
                    return test_case_func(*args,**kwargs)
                elif  testcase == 'jobStreamNegative':
                    print('IWRefresh test case started at: %s',datetime.datetime.now() )
                    return test_case_func(*args,**kwargs)
            return(inner)
        return(decorator)
    
        
    def get_job_stream_dependency(sequence_name):
        recursive_job_list=[]
        job_list = Read_conf.Read_job_list()  
        for job in job_list:
            if job['DEPENDENCY_JOB'] == sequence_name:  
                recursive_job_list.append(job['JOB_NAME'])
                if job['JOB_TYPE'] == 'Sequence':
                    job_list_2 = Read_conf.Read_job_list()
                    for job_2 in job_list_2:  
                        if job['DEPENDENCY_JOB'] == job['JOB_NAME']:
                            recursive_job_list.append(job_2['JOB_NAME'])
        return recursive_job_list            
        
            
    @get_case_description('jobStreamPositive')
    def job_stream_positive_test(ds_id,ds_pwd,driver_sequence):

        ## validateion 1， driver sequence must run successfully
        print("driver_sequence:"+driver_sequence)
        rs = DS_Operation.Get_job_status(driver_sequence)
        print("Driver sequence run status:"+ rs[0].split(':')[1])
        status_code = rs[0].split('(')[1].split(')')[0]
        if status_code == '1' or status_code == '2':
            print("driver_sequence validate successfully")
        else:
            print("driver_sequence validate failed")
            
            
       ##validation 2, the dependency job list must all run successfully 
        dependency_jobs = Job_stream_test.get_job_stream_dependency(driver_sequence) 
        job_status_dict = dict()
        fail_count = 0
        for job in dependency_jobs:
            rs = DS_Operation.Get_job_status(job)
            status = rs[0].split('(')[1].split(')')[0]
            job_status_dict[job] = status
            if status == '3' or status == '99':
                fail_count +=1
        #print(fail_count)
        
        if fail_count != 0 :
            raise TestException.JobStreamError()
        else:
            print("validatie passed")

    
    @get_case_description('jobStreamNegative')
    def job_stream_nagative_test(ds_id,ds_pwd,driver_sequence):
        
        '''validateion 1， driver sequence will run failed'''
        print("driver_sequence:"+driver_sequence)
        rs = DS_Operation.Get_job_status(driver_sequence)
        print("Driver sequence run status:"+ rs[0].split(':')[1])
        status_code = rs[0].split('(')[1].split(')')[0]
        if status_code == '3':
            print("driver_sequence negative validate successfully")
        else:
            print("driver_sequence negative validate failed")
            
            
        '''validation 2, the dependency job which has the latest timestamp will have a failed status.''' 
        dependency_jobs = Job_stream_test.get_job_stream_dependency(driver_sequence) 
        job_status_list = []
        job_status_dict = dict()
        for job in dependency_jobs:
            rs = DS_Operation.Get_job_status(job)
            
            status = rs[0].split('(')[1].split(')')[0]
            job_status_dict[job] = status
            if status == '3' or status == '99':
                fail_count +=1
        #print(fail_count)
        
        if fail_count != 0 :
            raise TestException.JobStreamError()
        else:
            print("validatie passed")
    
    
if __name__ == "__main__":   
    #Job_stream_test.decoreate_test()
    pass