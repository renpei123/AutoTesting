# -*- coding: utf-8 -*-
import sys


def Job_stream_test(ds_id,ds_pwd,test_type):
    
    #get the test case info

    if test_type == "Positive":
        print("description")
        print("case action")
        print ("case expectation")
    #step 1: run related sequence job with correct parameters
    #step 2: get related sequence and parallel job status input to one table
    pass

def IW_refresh_test():
    pass

def Performance_test():
    pass

def ASCA_control_test():
    pass

def Data_accuracy_test(db_id,db_pwd,case_type):
    if case_type == "Positive":
        
    
    if 
    #step 1: check the status of related parallel job
    
    #step 2: check rowcount by run sql in source db
    
    #step 3: check target rowcount by run sql in target db
    pass

def Data_structure_test():
    pass


if __name__ == "__main__": 
    ###use of this module
            
    args = sys.argv
    testcase = args[0]
    if Job_stream_test:
        ds_id = args[1]
        ds_pwd = args[2]
        Job_stream_test(ds_id,ds_pwd)
        
        
    
    pass




