# -*- coding: utf-8 -*-
import Read_conf
import DS_Operation
from Job_stream_test import Job_stream_test
import configparser

def get_dependency_job_list(sequence_name):
    job_list = Read_conf.Read_job_list()
    job_stream_list = []
    for job in job_list:
        if job['DEPENDENCY_JOB'] == sequence_name:
            job_stream = job['JOB_NAME']+"@"+job['JOB_ID']+"@"+job['ASCA_CONTROL_POINT_ID']
            job_stream_list.append(job_stream)
    return job_stream_list        


def test_pre_action():
    
    ''' define how to run the driver job, if the job is datastage sequence
    run below code '''
    conf = configparser.ConfigParser()
    conf.read(filenames='conf/conf.ini', encoding='utf-8')
    driver = conf['driver']
    driver_type = driver['driver_type']
    job_stream_count = int(driver['job_stream_count'])
    input_parameter = driver['input_parameter']
    driver_sequence = driver['driver_job']
    
    '''the job_stream_count will decide how many parallel job stream can run parallelly,
    that means how many job stream parameter should be assign to the driver sequence '''
       
    
    if driver_type == 'DataStage':
        '''when the driver is dataStage assign necessary parameter to the driver job '''
        job_stream_params = ['' for i in range(job_stream_count)]
        job_stream_list = get_dependency_job_list(driver_sequence)
        for i in range(len(job_stream_list)):
            param_index = i%job_stream_count
            job_stream_params[param_index] += job_stream_list[i]+','         
            ''' generate other parameters '''
            other_params = dict ()
            other_params_list = input_parameter.split(',')
        for param in other_params_list:
            other_params[param.split('=')[0]] = param.split('=')[1]
        print (other_params)    
            
        ''' send the job_stream_params to the driver sequence to run, input other parameters if necessary '''
        DS_Operation.Run_ds_job_on_windows(driver_sequence,job_stream_params,**other_params)  
            
    #''' if the driver is shell, should trigger the shell script with the necessary parameter '''
    elif driver_type == 'Shell':  
        pass
    else:
        pass


if __name__ == "__main__": 
     
    ###step 1 run pre-test action:run sequence job with correct parameter
    print('Running positive test process')
    print('step 1 run pre-test action:run sequence job with correct parameter')
    test_pre_action()
    
    ####step 2 do the job stream positive test case
    conf = configparser.ConfigParser()
    conf.read(filenames='conf/conf.ini', encoding='utf-8')
    driver = conf['driver']
    driver_sequence = driver['driver_job']
    test_type = conf['test']['test_type']
    if test_type == 'positive':
        Job_stream_test.job_stream_positive_test('driver_sequence')



    
    
    
    
    
    

    
    
    
    
    
    
