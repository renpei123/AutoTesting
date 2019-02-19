# -*- coding: utf-8 -*-
import os
#import sys
#import regex
#import shutil
#import Read_conf
from Read_conf import ReadConfig


def Get_job_status(ds_id,ds_pwd,job_name):
    conf = ReadConfig()
    host_info = conf.Read_DS_host()
    cmd_path  = conf.Read_DS_command_path()
    cmd_str = cmd_path + 'dsjob' + ' -domain ' + host_info['domain'] + ' -user ' + ds_id +' -password ' +ds_pwd \
    +' -server ' + host_info['host'] +' -jobinfo '  \
    +' ' + host_info['project'] +' '+job_name 
    cmd_str += '\n'
    print("DataStage command: "+cmd_str.replace(ds_pwd,'********'))
    rs = os.popen(cmd=cmd_str, mode='r')
    status_result =rs.readlines()
    status_dict = dict()
    #dict['Job Name']=job_name
    for i in range(len(status_result)):
        key = status_result[i].split('\t:')[0]
        value = status_result[i].split('\t:')[1].strip().replace('\n','')
        status_dict[key]=value
    report_dict= dict({job_name:status_dict})    
    print(report_dict)
    return report_dict


def Get_job_status_batch():
    pass


def Run_ds_job_on_windows(usr,password,job_name,job_stream_params,**kw):
    conf = ReadConfig()
    host_info = conf.Read_DS_host()
    cmd_path = conf.Read_DS_command_path()
    job_stream_parameter_list = conf.Read_job_stream_parameter_name_list()
    
    ########assign job stream to the driver job
    job_stream_count = len(job_stream_params)
    job_stream_appendix=''
    for i in range(len(job_stream_parameter_list)):
        job_stream= ' -param '+job_stream_parameter_list[i]+'='+ '"'+job_stream_params[i] +'"'
        job_stream_appendix+= job_stream
    #print(job_stream_appendix)  
    
    ##########assign other input parameter to the driver job
    params_appendix =''
    if len(kw) != 0:
        for key in kw:
            param = ' -param '+ key + '=' + '"' + kw[key]+'"'
            params_appendix +=param
    print(params_appendix)        
    cmd_str = cmd_path + 'dsjob' + ' -domain ' + host_info['domain'] + ' -user ' + usr +' -password ' +password \
    +' -server ' + host_info['host'] +' -run -wait -mode NORMAL ' + job_stream_appendix + params_appendix \
    +' ' + host_info['project'] +' '+job_name 
    cmd_str += '\n'
    print("DataStage command: "+cmd_str.replace(password,'********'))
    rs = os.popen(cmd=cmd_str, mode='r')
    print(rs.readlines())
    return rs
   

def Run_ds_job_on_linux(job_name):
    
    host_info = Get_DS_host_info()
    cmd_path  = Get_DS_host_cmd_path()
    cmd_str = cmd_path + 'dsjob' + '-domain ' + host_info['domain'] + '-user ' + host_info['user'] +'-password ' +host_info['password'] +'-server ' + host_info['host'] + '-run ' + job_name 
    cmd_str += '\ndir'
    print("DataStage command: "+cmd_str)
    rs = os.popen(cmd=cmd_str, mode='r')
    print(rs.readlines())
    
   
   
def Get_job_stream_count_from_job():
    pass
   


if __name__ == "__main__":
    pass
   #print("Get_job_status_start")
   # Get_job_status('LD_IW_CONTROL_BDW_JobSeq')
