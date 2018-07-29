import os
import sys
import configparser
import shutil

conf = configparser.ConfigParser()
conf.read(filenames='conf/conf.ini', encoding='utf-8')
host_info = conf['host']
cmd_path = conf['sys']['command_path']

def jobstatus(job_name):
    '''
    Get the job's running status for a given job name
    '''
    cmd_str = '{0}dsjob -domain {1} -user {2} -password {3} -server {4} -jobinfo {5} {6}' \
        .format(cmd_path, host_info['domain'], host_info['user'],
                host_info['password'], host_info['host'], host_info['project'], job_name)
    #print(cmd_str)
    comm = os.popen(cmd=cmd_str, mode='r')
    dic = dict()
    for line in comm.readlines():
        lines = line.split(':', 1)
        key = lines[0].strip()
        value = lines[-1].strip()
        dic[key] = value
    return dic


def createDependency():
    Jobs_Dependency = dict()
    Jobs_Dependency['LD_RDMSTG_CAMSS_ZOS_JobSeq'] = ['LD_RDMSTG_CAMSS_SOLUTION_ISA_ZOS_From_XML_PJob']
    Jobs_Dependency['LD_RDMSTG_CAMSS_PDA_JobSeq'] = ['LD_RDMSTG_CAMSS_SOLUTION_ISA_PDA_From_ZOS_PJob']
    print(Jobs_Dependency)
    return Jobs_Dependency


    ###parallel is a list
def positiveJobStreamTest(sequence,parallel,job_report):
    '''
    For jobStream Test
    '''

    '''
    Positive test case
    '''
    seq_info = job_report[sequence]
    testResult = 'Success'
    if seq_info['Job Status'] == 'RUN OK (1)':
        print('Sequence job %s Status is Run OK,check the parallel jobs status...' % sequence)
        for pjob in parallel:
            pjob_info = job_report[pjob]
            if pjob_info['Job Status'] == 'RUN OK (1)' or 'RUN WARN (2)':
                print('Parallel job %s Status is Run OK' % pjob)
                continue
            else:
                testResult = 'Failed'
                break
        if testResult == 'Success':
            print("Parallel jobs run finished successfully when sequence job run finished, the test case Passed")
        else:
            print('Parallel job run failed when Sequence job run OK,the Job Stream test Failed')
    return testResult



    ###parallel is a list
def negativeJobStreamTest(sequence,parallel,job_report):
    '''
    Negative Test case
    '''
    seq_info = job_report[sequence]
    testResult = 'Success'
    if seq_info['Job Status'] != 'RUN OK (1)' or 'RUN WARN (2)':
        print('Sequence job %s Status is ABORT,check the parallel jobs status...' % sequence)
        for pjob in parallel:
            flag=0
            pjob_info = job_report[pjob]
            if pjob_info['Job Status'] == 'RUN OK (1)' or 'RUN WARN (2)':
                print('Parallel job %s Status is Run OK' % pjob)
                continue
            else:
                flag = 1
                break
        if flag == 1:
            print("Parallel jobs run finished successfully when sequence job run finished, the test case Passed")
        else:
            print('Parallel job run failed when Sequence job run OK,the Job Stream test Failed')
            testResult = 'Failed'
    return testResult


#####Step 1, Generate the dependency

Job_Dependency = createDependency()
##Generate job list base on dependency
job_list = []
for sequence in Job_Dependency:
    parallel = Job_Dependency[sequence]
    job_list.append(sequence)
    job_list.extend(parallel)
print(job_list)
job_report=dict()
for job in job_list:
    job_report[job] = jobstatus(job)
print(job_report)

with open('conf/tmp/job_report.txt','w') as comm:
	comm.write(str(job_report))

  
######Step 3 Job Stream validate
for sequence in Job_Dependency.keys():
    parallel = Job_Dependency[sequence]
    positiveJobStreamTest(sequence, parallel, job_report)
    negativeJobStreamTest(sequence, parallel, job_report)












