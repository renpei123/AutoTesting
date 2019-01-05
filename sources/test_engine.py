# -*- coding: utf-8 -*-
#run python test_engine.py test_case_name test_case_type **necessary_args


from Job_stream_test import Job_stream_test
from  Data_accuracy_test import Data_accuracy_test
import test_pre_action
import Read_conf
#import unittest
import sys


if __name__ == "__main__": 
    args = sys.argv
    print(args[1])
    if args[1] == 'positive_test_pre_action':
        test_pre_action.test_pre_action(args[2],args[3])
    elif args[1] == 'job_stream_test':
        if args[2] == 'positive':
            driver_sequence = Read_conf.Read_Driver_Sequence()
            ds_id = args[3]
            ds_pwd = args[4]
            Job_stream_test.job_stream_positive_test(ds_id,ds_pwd,driver_sequence)
        elif args[1] == 'nagative':
            Job_stream_test.job_stream_positive_test()
        else:
            print('The test type is not valid')
    elif args[0] ==  'data_accuracy_test':
        if args[1] == 'rowcount':
            Data_accuracy_test.Row_count_positive_test()
        elif args[1] == 'sample_data':
            Data_accuracy_test.Sample_data_positive_test()
        else:
            print('The test case is not valid')
    else: 
        print('The test case is not valid,please check your parameters')        





