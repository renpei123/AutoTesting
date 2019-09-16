# -*- coding: utf-8 -*-
#run python test_engine.py test_case_name test_case_type **necessary_args

import sys
import os

from test_case.Job_stream_test import Job_stream_test
from Common.TestException import ASCAControlError
from Common.TestException import JobStreamError
from test_case.IWRefresh_test import IWRefresh_test
from test_case import test_pre_action
from test_case.ASCA_test import ASCA_test
from Common.Read_conf import ReadConfig
from test_case.Rowcount_test import Rowcount_test
from Common.TestException import RowcountError
#import unittest



def main_job(args):
    if args[1] == 'positive_test_pre_action':
        test_pre_action.test_pre_action(args[2], args[3], args[4])
        return
    
    if args[1] == 'job_stream_test':
        if args[2] == 'positive':
            conf = ReadConfig()
            driver_sequence = conf.Read_Driver_Sequence()
            job_stream_test = Job_stream_test()
            print("driver_sequence:"+driver_sequence)
            ds_node = args[3]
            ds_id = args[4]
            ds_pwd = args[5]
            try:
                job_stream_test.job_stream_positive_test(ds_node, ds_id, ds_pwd, driver_sequence)
            except JobStreamError as e:
                print(e.message)
                sys.exit(1)
        elif args[1] == 'negative':
            Job_stream_test.job_stream_positive_test()
        else:
            print('The test type is not valid')
        return

    if args[1] == 'iw_refresh_test':
        if args[2] == 'positive':
            iw_refresh_db_node = args[3]
            iw_db_user = args[4]
            iw_db_pwd = args[5]
            try:
                iw_test = IWRefresh_test()
                print('positive')
                iw_test.iwefresh_positive_test(iw_refresh_db_node, iw_db_user, iw_db_pwd)
            except JobStreamError as e:
                print(e.message)
                sys.exit(1)
        elif args[1] == 'negative':
            iw_test = IWRefresh_test()
            iw_test.iwefresh_negative_test()
        else:
            print('The test type is not valid')
        return

    if args[1] == 'asca_control_test':
            uid = args[2]
            pwd = args[3]
            try:
                asca_test = ASCA_test()
                conf = ReadConfig()
                asca_db_node = conf.Read_asca_db_node()
                asca_test.asca_test(asca_db_node,uid, pwd)
            except ASCAControlError as e:
                print(e.message)
                sys.exit(1)
            return


    if args[1] == 'rowcount_test':
        asca_uid = args[2]
        asca_pwd = args[3]
        try:
            rowcount_test=Rowcount_test()
            conf = ReadConfig()
            asca_db_node = conf.Read_asca_db_node()
            Rowcount_test.rowcount_test(asca_db_node,asca_uid,asca_pwd)
        except RowcountError as e:
            print(e.message)
            sys.exit(1)
        return
    else:
        print('The test case is not valid,please check your parameters')


if __name__ == "__main__":
    sys.path.append("..")
    args = sys.argv
    main_job(args)
    
 
    





