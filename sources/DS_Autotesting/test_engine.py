# -*- coding: utf-8 -*-
#run python test_engine.py test_case_name test_case_type **necessary_args


from Job_stream_test import Job_stream_test
from  Data_accuracy_test import Data_accuracy_test
from TestException import JobStreamError
import test_pre_action
from Read_conf import ReadConfig
#import unittest
import sys

def main_job(args):
    if args[1] == 'positive_test_pre_action':
        test_pre_action.test_pre_action(args[2],args[3])
        return
    
    if args[1] == 'job_stream_test':
        if args[2] == 'positive':
            conf = ReadConfig()
            driver_sequence = conf.Read_Driver_Sequence()
            #print("driver_sequence:"+driver_sequence)
            ds_id = args[3]
            ds_pwd = args[4]
            try:
                Job_stream_test.job_stream_positive_test(ds_id,ds_pwd,driver_sequence)
            except JobStreamError as e:
                print(e.message)
                sys.exit(1)
        elif args[1] == 'nagative':
            Job_stream_test.job_stream_positive_test()
        else:
            print('The test type is not valid')
        return
    
    if args[0] ==  'data_accuracy_test':
        if args[1] == 'rowcount':
            Data_accuracy_test.Row_count_positive_test()
        elif args[1] == 'sample_data':
            Data_accuracy_test.Sample_data_positive_test()
        else:
            print('The test case is not valid')
        return
    
    print('The test case is not valid,please check your parameters')  


if __name__ == "__main__": 
    args = sys.argv
    main_job(args)
    
 
    





