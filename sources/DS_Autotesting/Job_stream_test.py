# -*- coding: utf-8 -*-
import DS_Operation
from Read_conf import ReadConfig
import TestException
import datetime
from generate_report import Generate_report


class Job_stream_test:
    
    def get_case_description(testcase):
        '''decorate function'''    
        def decorator(test_case_func):
            def inner(*args, **kwargs):
                if testcase == 'jobStreamPositive':
                    rc = ReadConfig()
                    print('Job Stream test case started at:%s' % datetime.datetime.now() )
                    with open(rc.read_job_stream_test_description(),'r',encoding='utf-8') as f:
                        description = f.read()
                        print(description)
                    return test_case_func(*args,**kwargs)
                elif testcase == 'jobStreamNegative':
                    print('Job stream negative test case started at: %s',datetime.datetime.now() )
                    return test_case_func(*args,**kwargs)
            return(inner)
        return(decorator)
    
        
    def get_job_stream_dependency(self, sequence_name):
        recursive_job_list=[]
        conf = ReadConfig()
        job_list = conf.Read_job_list()  
        for job in job_list:
            if job['DEPENDENCY_JOB'] == sequence_name:  
                recursive_job_list.append(job['JOB_NAME'])
                if job['JOB_TYPE'] == 'Sequence':
                    job_list_2 = conf.Read_job_list()
                    for job_2 in job_list_2:  
                        if job_2['DEPENDENCY_JOB'] == job['JOB_NAME']:
                            recursive_job_list.append(job_2['JOB_NAME'])

        print("Dependent job list" + str(recursive_job_list))
        return recursive_job_list

    @get_case_description('jobStreamPositive')
    def job_stream_positive_test(self, ds_id, ds_pwd, driver_sequence):

        ## validateion 1， driver sequence must run successfully
        print('\n Step 1, check the run status of the driver sequence job')
        gr = Generate_report()
        print("driver_sequence:"+driver_sequence + "\n")
        print("Run DataStage command on DataStage server:")
        job_status = DS_Operation.Get_job_status(ds_id,ds_pwd, driver_sequence)
        #print(job_status)
        gr.Append_job_status_to_report('jobstream_positive',job_status)
        status_code = job_status[driver_sequence]['Job Status']
        start_time = job_status[driver_sequence]['Job Start Time']
        end_time = job_status[driver_sequence]['Last Run Time']
        print("Driver sequence run status:" + status_code + " from " +start_time + " to " +end_time)
        if status_code == 'RUN OK (1)' or status_code == 'RUN OK (1)':
            print("The driver sequence run finished successfully, do next validate...")
        else:
            print("driver_sequence validate failed,the job stream test failed")
            raise TestException.JobStreamError
            
            
       ##validation 2, the dependency job list must all run successfully

        print("\nstep 2: check the status of jobs which dependent on the driver sequence job \n")
        dependency_jobs = self.get_job_stream_dependency(driver_sequence)
        fail_count = 0
        for i in range(len(dependency_jobs)):
            job = dependency_jobs[i]
            print("\n %d . %s" % (i+1, job))
            job_status = DS_Operation.Get_job_status(ds_id, ds_pwd, job)
            status = job_status[job]['Job Status']
            start_time = job_status[job]['Job Start Time']
            end_time = job_status[job]['Last Run Time']
            print("Job Status: %s" % status + " from "+start_time + " to " + end_time)
            gr.Append_job_status_to_report('jobstream_positive',job_status)
            if status == 'RUN FAILED(3)' or status == '99':
                fail_count +=1
        #print(fail_count)
        if fail_count != 0 :
            print("\nWhen the driver job run finished successfully,one or more dependent jobs run failed, check the job status report "
                  "for the detail,job stream test failed")
            raise TestException.JobStreamError()
        else:
            print("\nWhen the driver job run finished successfully, all the dependent job run finished successfully, the job stream test "
                  "run pass")

    
    @get_case_description('jobStreamNegative')
    def job_stream_nagative_test(self,ds_id,ds_pwd,driver_sequence):
        
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
        #job_status_list = []
        job_status_dict = dict()
        for job in dependency_jobs:
            rs = DS_Operation.Get_job_status(ds_id,ds_pwd,job)
            status = rs[job]['Job Status']
            job_status_dict[job] = status
            if status == '3' or status == '99':
                fail_count +=1
        #print(fail_count)
        
        if fail_count != 0 :
            print("When the driver job run finished successfully,one or more dependent jobs run failed, check the job status report "
                  "for the detail,job stream test failed")
            raise TestException.JobStreamError()
        else:
            print("When the driver job run finished successfully, all the dependent job run finished successfully, the job stream test "
                  "run pass")
    
    
if __name__ == "__main__":
    js = Job_stream_test()
    js.job_stream_positive_test('dsdev', 'Jan2019Jan', 'LD_RDMSTG_GBS_RESOURCE_JobSeq')
    #js.get_job_stream_dependency2('LD_RDMSTG_GBS_RESOURCE_JobSeq')
    #get_job_stream_dependency()