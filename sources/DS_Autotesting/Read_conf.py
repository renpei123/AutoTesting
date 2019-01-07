# -*- coding: utf-8 -*-
import xlrd
#import json
import configparser



def convert_xlsx_to_dict(file_name):
    data = xlrd.open_workbook(file_name)
    table = data.sheets()[0]
    nrows = table.nrows
    columns = table.row_values(0)
    #print (columns)
    result_list = []
    for i in range(1,nrows):
        value = table.row_values(i)
        row = dict()        
        for i in range(len(columns)):
            row[columns[i]] = value[i]
        #jsonResult = json.dumps(row)
        result_list.append(row)
    return result_list
    

def Read_job_list():
    ##get table list file
    file = "sources/DS_AutoTesting/job_info.xlsx"
    #trigger the convert function to read the data to a jsonObject
    job_list = convert_xlsx_to_dict(file)
    return job_list
    
    
def Read_table_list():
    ##get job list file
    file = "sources/DS_AutoTesting/table_info.xlsx"
    #trigger the convert function to read the data to a jsonObject
    table_list = convert_xlsx_to_dict(file)
    return table_list

def Read_Driver_Sequence():
    conf = configparser.ConfigParser()
    conf.read(filenames='sources/DS_AutoTesting/conf/conf.ini', encoding='utf-8')
    driver_sequence = conf['driver']['driver_job']
    return driver_sequence
    


