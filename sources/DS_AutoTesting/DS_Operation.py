# -*- coding: utf-8 -*-
import os
#import sys
import configparser
#import regex
#import shutil



conf = configparser.ConfigParser()
conf.read(filenames='conf/conf.ini', encoding='utf-8')
host_info = conf['host']
dir_info = conf['dir']
cmd_path = conf['sys']['command_path']
jobs_dir = dir_info['jobs_dir']

def Get_job_status(job_name):
    
    cmd_str = cmd_path + 'dsjob' + ' -domain ' + host_info['domain'] + ' -user ' + host_info['user'] +' -password ' +host_info['password'] \
    +' -server ' + host_info['host'] +' -jobinfo '  \
    +' ' + host_info['project'] +' '+job_name 
    cmd_str += '\n'
    print(cmd_str)
    rs = os.popen(cmd=cmd_str, mode='r')
    status_result =rs.readlines()
    print(status_result)
    return status_result


def Get_job_status_batch():
    pass


def Run_ds_job_on_windows(usr,password,job_name,job_stream_params,**kw):
    #print(job_name)
    
    ########assign job stream to the driver job
    job_stream_count = len(job_stream_params)
    job_stream_appendix=''
    for i in range(job_stream_count):
        job_stream= ' -param Job_Run_Stream_' +str(i) + '='+ '"'+job_stream_params[i] +'"'
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
    print(cmd_str)
    rs = os.popen(cmd=cmd_str, mode='r')
    print(rs.readlines())
    return rs
   

def Run_ds_job_on_linux(job_name):
    cmd_str = cmd_path + 'dsjob' + '-domain ' + host_info['domain'] + '-user ' + host_info['user'] +'-password ' +host_info['password'] +'-server ' + host_info['host'] + '-run ' + job_name 
    cmd_str += '\ndir'
    print(cmd_str)
    rs = os.popen(cmd=cmd_str, mode='r')
    print(rs.readlines())
    
   
   
def Get_job_stream_count_from_job():
    pass
   


if __name__ == "__main__":
    print(Run_ds_job_on_windows('LD_IW_CONTROL_BDW_JobSeq',[]))
