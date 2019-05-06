# -*- coding: utf-8 -*-

#this test is to validate if the test id tadmin has permission to all the base table

import common_validate
import get_config


def base_table_permission_test(id,pwd):
    
    #step 1 get base table list
    #print('Get table List:')

    tableList=get_config.getBaseTableList()
    print('Base table list:'+str(tableList))
    
    
    #step 2 define the file name to which the test result write in
    fileName = ('tmp/Base_table_permission_validation_result.csv')
       
    #step 2 input base table as the tableList, start the validation
    print('starting the base table validation...')
    testResult = common_validate.permitValidation(id,pwd,tableList,fileName)
    if testResult == "Pass":
        print('the test case Passed, the ID "tadmin" has the permission to all the base table under the list, '
          +'detail report please view the result file '+ fileName)
    elif testResult == "Failed":
        print('the test case Failed, the ID "tadmin" does not have the permission to all the base table under the list, '
          +'detail report please view the result file '+ fileName)       
    
 
def world_wide_view_permission_test():
    #step1 get world_wide_view list
    viewList=get_config.getViewList('V');
    print('world vide view list:'+str(viewList))
    
    #step 2 define the file name to which the test result write in
    fileName = ('tmp/World_wide_view_permission_validation_result.csv')     
    
    #step 3 input base table as the tableList, start the validation
    print('starting the world wide view validation...')
    testResult = common_validate.permitValidation('tadmin','oct18oct',viewList,fileName)
    if testResult == "Pass":
        print('the test case Passed, the ID "twwview" has the permission to all the world wide view under the list, '
          +'detail report please view the result file '+ fileName)
    elif testResult == "Failed":
        print('the test case Failed, the ID "twwview" does not have the permission to all the world wide view under the list, '
          +'detail report please view the result file '+ fileName)   
    
 
def regular_view_permission_test():
    #step1 get world_wide_view list
    viewList=get_config.getViewList('UV');
    print('regular view list:'+str(viewList))
    
    #step 2 define the file name to which the test result write in
    fileName = ('tmp/Regular_view_permission_validation_result.csv')
       
   #step 3 input base table as the tableList, start the validation
    print('starting the regular view validation...')
    testResult = common_validate.permitValidation('twwview','oct18oct',viewList,fileName)
    if testResult == "Pass":
        print('the test case Passed, the ID "twwview" has the permission to all the world wide view under the list, '
          +'detail report please view the result file '+ fileName)
    elif testResult == "Failed":
        print('the test case Failed, the ID "twwview" does not have the permission to all the world wide view under the list, '
          +'detail report please view the result file '+ fileName)  
        
        
        
        

if __name__ == "__main__":
    #base_table_permission_test()
    #world_wide_view_permission_test()
    #regular_view_permission_test()
    
    #####1. Base table permission positive test case
    print('------------- Base table permission positive test case---------------------')
    print('------------- Test Description---------------------------------------------')
    print('This is the positive test case for Test Admin IDs (tadmin) to ensure they have access to the base table(s) and to perform the row count. \n'+ 
          'The expected number of rows in base table will be used as the baseline to validate the test result compares with 4.2, 4.3, 4.6 test case.') 
    print('--------------Test Action--------------------------------------------------')
    print('Use the Test Admin ID (tadmin) to perform the select count SQL against the base table(s) on PDA environment.')
    print ('-------------expected ----------------------------------------------------')
    print ('The test ID "tadmin" should have the access to all the base table under the scope\n')
   
    print('Starting test...')
    print('run the function base_table_permission_test()  with the correct ID "tadmin"')
    base_table_permission_test('tadmin','oct18oct')
    
    
    
    
    #######2	Worldwide View(s) Validation Test
    print('------------- world wide views permission positive test case---------------------')
    print('------------- Test Description---------------------------------------------')
    print('This is the positive test case for worldwide access against the *_V to ensure permission to *_V is granted') 
    print('--------------Test Action--------------------------------------------------')
    print('Use the Test Worldwide view ID (twwview) to perform the select count SQL against the *_V on PDA environment.')
    print ('-------------expected ----------------------------------------------------')
    print ('The test ID "twwview" should have the access to all the worldwide view *.V\n')
    
    print('Starting test...')
    print('run the function base_table_permission_test()  with the correct ID "twwview"')
    world_wide_view_permission_test('twwview','oct18oct')
    
    
    print('------------- world wide views permission nagative test case---------------------')
    print('------------- Test Description---------------------------------------------')
    print('This is the negative test case for worldwide access against the *_UV to ensure permission to *_UV is not granted.')
    print('--------------Test Action--------------------------------------------------')
    print('Use the Test Worldwide view ID (twwview) to perform the select count SQL against the *_UV on PDA environment.')
    print ('-------------expected ----------------------------------------------------')
    print ('The test ID "twwview" should not have the access to any regular view *.UV\n')
    print('Starting test...')
    print('run the function regular_view_permission_test()  with the incorrect ID "twwview"')
    regular_view_permission_test('twwview','oct18oct')
    
    
    
    #######3	Regular View(s) Validation Test
    print('------------- Regular views permission positive test case---------------------')
    print('------------- Test Description---------------------------------------------')
    print('This is the positive test case for Regular access against the *_UV to ensure permission to *_UV is granted') 
    print('--------------Test Action--------------------------------------------------')
    print('Use the Test Regular view ID (tregview) to perform the select count SQL against the *_UV on PDA environment.')
    print ('-------------expected ----------------------------------------------------')
    print ('The test ID "tregveiw" should have the access to all regular view *.UV\n')
    print('Starting test...')
    print('run the function regular_view_permission_test()  with the correct ID "tregview"')
    regular_view_permission_test('tregview','oct18oct')
    
    
    print('------------- world wide views permission nagative test case---------------------')
    print('------------- Test Description---------------------------------------------')
    print('This is the negative test case for worldwide access against the *_V to ensure permission to *_V is not granted.') 
    print('--------------Test Action--------------------------------------------------')
    print('Use the Test Regular view ID (tregview) to perform the select count SQL against the *_V on PDA environment.')
    print ('-------------expected ----------------------------------------------------')
    print ('The test ID "tregveiw" should not have the access to any worldwide view *.V\n')
    
    print('Starting test...')
    print('run the function world_wide_view_permission_test()  with the incorrect ID "tregview"')
    world_wide_view_permission_test()
    
    
    #######after test generate the access report
    print('generating access report')
    
    
    
    
    
    
    
    
    
    
    

