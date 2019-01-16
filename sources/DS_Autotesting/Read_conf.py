# -*- coding: utf-8 -*-
import xlrd
#import json
import configparser

class ReadConfig:
    
    job_list_file = 'sources/DS_AutoTesting/job_info.xlsx'
    table_list_file = 'sources/DS_AutoTesting/table_info.xlsx'
    config_file = 'sources/DS_AutoTesting/conf/conf.ini'
    
    def convert_xlsx_to_dict(self,file_name):
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
        
    
    def Read_job_list(self):
        ##get table list file
        #file = "sources/DS_AutoTesting/job_info.xlsx"
        #trigger the convert function to read the data to a jsonObject
        job_list = self.convert_xlsx_to_dict(self.job_list_file)
        return job_list
        
        
    def Read_table_list(self):
        ##get job list file
        #file = "sources/DS_AutoTesting/table_info.xlsx"
        #trigger the convert function to read the data to a jsonObject
        table_list = self.convert_xlsx_to_dict(self.table_list_file)
        return table_list
    
    def Read_Driver_Sequence(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        driver_sequence = conf['driver']['driver_job']
        return driver_sequence
    
    def Read_DS_host(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        #driver_sequence = conf['driver']['driver_job']
        return conf['host']
    
    def Read_DS_command_path(self):
        
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        #driver_sequence = conf['driver']['driver_job']
        return conf['sys']['command_path']
    def Read_Driver(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        #driver_sequence = conf['driver']['driver_job']
        return conf['driver']
  
if __name__ == "__main__":   
    #Job_stream_test.decoreate_test()
    conf =   ReadConfig()
    f=conf.Read_Driver()
    g=conf.Read_DS_host()
    print(f['driver_job'])  
    print(g)


