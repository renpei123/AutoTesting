"""
create by: Fu Qiang Zhang(fqzhang@cn.ibm.com)
modified by: Ya Huang(huangycd@cn.ibm.com)
last modification: 2017-12-12,Tuesday
desc:
1. list jobs for a datastage project
2. use this list to export all data datastage jobs into separate dsx files
3. categorize all dsx files into corresponding folders
"""

import os
import sys
import configparser
import regex
import shutil

current_path = os.path.dirname(os.path.realpath(__file__))
conf_path = os.path.join(current_path, 'conf/conf.ini')
job_list_path = os.path.join(current_path, 'conf/job_list')
conf = configparser.ConfigParser()
conf.read(conf_path, encoding='utf-8')
host_info = conf['host']
dir_info = conf['dir']
cmd_path = conf['sys']['command_path']
jobs_dir = dir_info['jobs_dir']



def check_file_exist(file):
    return os.access(path=file, mode=os.F_OK)


def export(ds_user, ds_pwd, job_list_file = job_list_path, begin_line=0, end_line=None):
    '''
    read job list from conf/job_list.ini file
    then export all in the list to dsx files
    '''
	
    print('Starting export')
    print(ds_user)
    cnt = int(conf['dir']['exported']) if str(conf['dir']['exported']).isnumeric() else 0
    jl = open(file=job_list_path, mode='r').readlines()
    to_process = None
    if end_line is None:
        if cnt > begin_line:
            to_process = jl[cnt:]
            print(to_process)
        else:
            to_process = jl[begin_line:]
    else:
        if end_line < begin_line:
            print('error')
            return None
        elif (cnt > begin_line) and (cnt < end_line):
            to_process = jl[cnt:end_line]
        else:
            to_process = jl[begin_line:end_line]
    for job_name in to_process:
        job_name = str(job_name).rstrip('\n')
        job_file_name = job_name + '.dsx'
        if os.access(path=jobs_dir, mode=os.R_OK):
            if check_file_exist(jobs_dir + '/' + job_file_name):
                print(jobs_dir + '/' + job_file_name, ': Exported already')
                continue
            else:
                print('Exporting ', cnt + 1, '\t:\t', job_name)
                cmd_str = cmd_path + 'dsexport /D=' + host_info['domain'] + ' /H=' + host_info['host'] + ' /U=' + \
                    ds_user + ' /P=' + ds_pwd + ' /JOB=' + job_name + ' /NODEPENDENTS ' +'/EXEC /APPEND '+ \
                    host_info['project'] + ' ' + jobs_dir + '/' + job_file_name
                cmd_str += '\ndir'
                rs = os.popen(cmd=cmd_str, mode='r')
                print(rs.readlines())
                cnt += 1
                conf.set(section='dir', option='exported', value=str(cnt))
                conf.write(fp=open(file='C:\ACindy\Project\AutoDeploy\ExportMultiDSJobs-master/conf/conf.ini', mode='w'))
                print('exported: ', job_name, '\n')
        else:
            print('jobs dir is not readable')
            break


def read_job_names(ds_user,ds_pwd):
    '''
    list jobs of project
    and store the list to job_list file
    '''
    cmd_str = '{0}dsjob -domain {1} -user {2} -password {3} -server {4} -ljobs {5}'\
        .format(cmd_path, host_info['domain'], ds_user,
                ds_pwd, host_info['host'], host_info['project'])
    jobs = os.popen(cmd=cmd_str, mode='r')
    with open('conf/job_list', mode='w') as job_list_file:
        job_list_file.writelines(jobs.readlines())


def add_path(file_name):
    return jobs_dir + '/' + file_name


def categorize():
    os.chdir(jobs_dir)
    files = os.listdir(jobs_dir)
    files_full_path = list(map(add_path, files))
    for file_full_path in files_full_path:
        if not regex.search(pattern=r'(?<=\.dsx)$', string=file_full_path):
            continue
        else:
            dsx = open(file=file_full_path, mode='r')
            category = regex.compile(r'(?<=^      Category ").+(?=")')
            for line in dsx.readlines():
                matched = category.search(line)
                if matched:
                    # create directory and move/copy the dsx files into target directory
                    directory = str(matched.captures()[0]).lstrip('\\\\').split('\\\\')[-1]
                    if not os.access(path='Jobs', mode=os.R_OK):
                        os.mkdir(path='Jobs')
                    if not os.access(path='Jobs/' + directory, mode=os.R_OK):
                        os.mkdir(path='Jobs/' + directory)
                    if os.access(path=file_full_path, mode=os.R_OK):
                        shutil.copy2(src=file_full_path, dst='Jobs/' + directory)
                else:
                    continue


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        operation = args[1]
        if operation == 'export':
            jobs_file = conf['dir']['job_list_file']
            print('Starting')
            print(jobs_file)
            export(args[2], args[3], jobs_file)
            print('End')
        elif operation == 'list':
            read_job_names(args[2],args[3])
        elif operation == 'categorize':
            categorize()
        else:
            print('invalid operation.')
    else:
        print('no arguments provided.')
