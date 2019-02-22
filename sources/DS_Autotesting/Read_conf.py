# -*- coding: utf-8 -*-
import xlrd
#import json
import configparser
import os
class ReadConfig:
    current_path = os.path.dirname(os.path.realpath(__file__))
    job_list_file = os.path.join(current_path, 'conf/job_info.xlsx')
    table_list_file = os.path.join(current_path, 'conf/table_info.xlsx')
    '''config_file is the one to manage all the process information which used in the whole auto testing'''
    config_file = os.path.join(current_path, 'conf/conf.ini')
    job_status_report_file = os.path.join(current_path, 'tmp/job_status_report.json')
    db_conf = os.path.join(current_path, 'conf/db.ini')
    job_stream_test_description_file = os.path.join(current_path, 'conf/job_stream_positive_test_description')
    iw_refresh_test_description_file = os.path.join(current_path, 'conf/iw_refresh_positive_test_description')
    job_stream_positive_status_report = os.path.join(current_path,'tmp/job_status_report.json')
    iw_refresh_status_report = os.path.join(current_path, 'tmp/IWRefresh_control_report.json')
    job_stream_positive_test_report = os.path.join(current_path,'report/job_stream_positive_test_report.xls')
    iw_refresh_positive_test_report = os.path.join(current_path,'report/iw_refresh_positive_test_report.xls')

    

    def convert_xlsx_to_dict_array(self,file_name):
        data = xlrd.open_workbook(file_name)
        table = data.sheets()[0]
        nrows = table.nrows
        columns = table.row_values(0)
        result_list = []
        for i in range(1,nrows):
            value = table.row_values(i)
            row = dict()        
            for i in range(len(columns)):
                row[columns[i]] = value[i]
            result_list.append(row)
        return result_list
    
    def Read_job_list(self):
        job_list = self.convert_xlsx_to_dict_array(self.job_list_file)
        return job_list
        
    def Read_table_list(self):
        table_list = self.convert_xlsx_to_dict_array(self.table_list_file)
        return table_list
    
    def Read_Driver_Sequence(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        driver_sequence = conf['driver']['driver_job']
        return driver_sequence
    
    def Read_DS_host(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        return conf['host']
    
    def Read_DS_command_path(self):
        
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        return conf['sys']['command_path']
    def Read_Driver(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file, encoding='utf-8')
        return conf['driver']

    def Read_source_db_node(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file,encoding='utf-8')
        return conf['db_node']['source_db_node']

    def Read_target_db_node(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file,encoding='utf-8')
        return conf['db_node']['target_db_node']

    def Read_iwrefresh_db_node(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file,encoding='utf-8')
        return conf['db_node']['iwrefresh_db_node']

    def Read_where_condition(self,table_nm):
        conf = configparser.ConfigParser()
        conf.read(self.config_file,encoding='utf-8')
        return conf['sample_data_condition'][table_nm]

    def Read_job_stream_parameter_name_list(self):
        conf = configparser.ConfigParser()
        conf.read(self.config_file,encoding='utf-8')
        job_stream_str = conf['driver']['job_stream_parameter_name']
        job_stream_param_list = job_stream_str.split(',')
        return job_stream_param_list

    
    def Read_job_status_report(self):
        with open(self.job_status_report_file,'r') as f:
            lines = f.readlines()
        for line in lines:
            status_dict = eval(line)
        return status_dict

    '''the function will read the db config info base on the db_node'''
    def Read_db_config(self,db_node):
        conf = configparser.ConfigParser()
        conf.read(self.db_conf,encoding='utf-8')
        return conf[db_node]

    def read_job_stream_test_description(self):
        return self.job_stream_test_description_file

    def read_iw_refresh_test_description(self):
        return self.iw_refresh_test_description_file

    def read_stream_positive_status_report_file(self):
        return self.job_stream_positive_status_report

    def read_iw_refresh_status_report_file(self):
        return self.iw_refresh_status_report

    def read_job_stream_positive_test_report(self):
        return self.job_stream_positive_test_report
    def read_iw_refresh_positive_test_report(self):
        return self.iw_refresh_positive_test_report



if __name__ == "__main__":   
    #print(ReadConfig.job_list_file)
    conf = ReadConfig()
    print(conf.Read_job_stream_parameter_name_list())
    print(conf.read_iw_refresh_test_description())
    # print(conf.Read_job_status_report())
    #db_node = 'bluedb2'
    #db = conf.Read_db_config(db_node)
    #print(db['driver'])
    #print()



