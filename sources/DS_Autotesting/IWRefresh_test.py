# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 16:30:03 2019

@author: RongHe
"""

# -*- coding: utf-8 -*-
from Read_conf import ReadConfig
import TestException
import datetime
import db_connect
from generate_report import Generate_report


class IWRefresh_test:
    MonthEnum = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
                 'Nov': 11, 'Dec': 12}

    def job_status_time_transfer(self, date_time_string):
        #str = "Wed Nov 22 06:30:00 2017"
        str = date_time_string
        date_format = str.split(' ')
        year = int(date_format[4])
        month = self.MonthEnum[date_format[1]]
        day = int(date_format[2])
        hour = int(date_format[3].split(':')[0])
        minute = int(date_format[3].split(':')[1])
        second = int(date_format[3].split(':')[2])
        run_time = datetime.datetime(year, month, day, hour, minute, second)
        return run_time

    def get_case_description(testcase):
        '''decorate function'''

        def decorator(test_case_func):
            def inner(*args, **kwargs):
                if testcase == 'IWRefresh_positive':
                    rc = ReadConfig()
                    print('IW Refresh positive test case started at:%s' % datetime.datetime.now())
                    with open(rc.read_iw_refresh_test_description(),'r',encoding='utf-8') as f:
                        description = f.read()
                    print(description)
                    return test_case_func(*args, **kwargs)
                elif testcase == 'IWRefresh_negative':
                    print('IWRefresh negative test case started at: %s', datetime.datetime.now())
                    return test_case_func(*args, **kwargs)

            return (inner)

        return (decorator)



    @get_case_description("IWRefresh_positive")
    def iwefresh_positive_test(self,iwrefresh_uid,iwrefresh_pwd):
        '''read config file for the job stream'''
        conf = ReadConfig()
        iwrefresh_db_node = conf.Read_iwrefresh_db_node()
        job_list = conf.Read_job_list()
        job_status_report = conf.Read_job_status_report()
        job_iw_control_report = []
        iw_refresh_failed_count = 0
        for job in job_list:
            data_group = job['DATAGROUP_ID']
            iw_refresh_control_status = dict()
            if data_group != '':
                job_name = job['JOB_NAME']
                job_run_status = job_status_report[job_name]['Job Status']
                job_start_time = self.job_status_time_transfer(job_status_report[job_name]['Job Start Time'])
                job_end_time = self.job_status_time_transfer(job_status_report[job_name]['Last Run Time'])
                '''step 1 validate if the parallel job show pass'''
                print("step 1: validate the run status of job: %s ..." % (job_name) +" \nstart time:" +str(job_start_time)+"\nend time:"\
                      + str(job_end_time))
                print("----------------------------------------------------------------------------------")
                if job_run_status == 'RUN OK (1)' or job_run_status == 'RUN OK (1)':
                    print("     the job status is %s,the status check passed,go to next step" % job_run_status)
                else:
                    print("The DataGroup Related job status is failed")
                    raise TestException.IWRefreshError()

                '''step 2 validate if the IW Refresh record shows pass and the IW Refresh start time big than job start time,
                    the end time is less than the end time '''
                '''get the bludb conf, and trige the db to run the sql'''

                print("step2: Get iw refresh status from iwrefresh db...")
                print("----------------------------------------------------------------------------------")
                print("Data group: %s" %data_group)
                sql = "select B.DATAGROUP_NM as DATAGROUP_NM,A.STAT as STAT,A.LOAD_START as LOAD_START," \
                      "A.LOAD_END as LOAD_END from XLSSTG.LOAD_STATUS A inner join XLSSTG.DATA_GROUP B on " \
                      "A.DATAGROUP_ID = B.DATAGROUP_ID " \
                      "where B.DATAGROUP_NM= '{}\' AND A.LOAD_START > '{}' ".format(data_group, job_start_time)
                rs = db_connect.exec_sql_common(iwrefresh_db_node, iwrefresh_uid,iwrefresh_pwd,  sql)
                print("RUNNING QUERY:%s" % sql)
                if len(rs) != 0:
                    iwrefresh_status = rs[0]['STAT']
                    iwrefresh_start_time = rs[0]['LOAD_START']
                    iwrefresh_end_time = rs[0]['LOAD_END']
                    '''gather info to report'''
                    iw_refresh_control_status['JOB_NM'] = job_name
                    iw_refresh_control_status['JOB_START_TIME'] = str(job_start_time)
                    iw_refresh_control_status['JOB_END_TIME'] = str(job_end_time)
                    iw_refresh_control_status['DATA_GROUP_NM'] = data_group
                    iw_refresh_control_status['IWREFRESH_START_TIME'] = str(iwrefresh_start_time)
                    iw_refresh_control_status['IWREFRESH_END_TIME'] = str(iwrefresh_end_time)
                    iw_refresh_control_status['IWREFRESH_STATUS_'] = iwrefresh_status
                    job_iw_control_report.append(iw_refresh_control_status)
                    print("IWRefresh status: %s" %iwrefresh_status)
                    '''1. check the iw refresh status'''
                    if iwrefresh_status == 'COMPLETE':

                        print('''\nWhen the job %s run finished, The data group \"%s\" shows \"%s\" ,the IW Refresh test passed
                              '''
                              % (job_name,data_group,iwrefresh_status))
                    else:
                        iw_refresh_failed_count+=1
                        print('''When the job %s run finished, The data group \"%s\" shows \"%s\" ,
                         the IW Refresh test passed''' % (job_name,data_group,iwrefresh_status))

                else:
                    iw_refresh_failed_count += 1
                    print("The IW Refresh control not be triggered when the job %s start, the IW Refresh test failed" % (job_name))
        
        '''generate the iw refresh report'''
        iw_report = Generate_report()
        iw_report.write_iwefresh_status_to_report(job_iw_control_report)
        iw_report.generate_iwrefresh_positive_report()

        if iw_refresh_failed_count != 0:
            print("one or more table's IWRefresh control failed, "
                  "check the iw_refresh_positive_test_report.xls for detail")
            raise TestException.IWRefreshError()

    @get_case_description("IWRefresh_negative")
    def iwefresh_negative_test(self):
        pass




if __name__ == "__main__":
   iw = IWRefresh_test()
   iw.iwefresh_positive_test('siwwebd', 'Bluemix_Jan18Jan')
