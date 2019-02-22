# -*- coding: utf-8 -*-
import json, xlwt

from Read_conf import ReadConfig
"""
Created on Fri Jan 18 17:59:57 2019

@author: RongHe
"""

class Generate_report:
    conf = ReadConfig()
    job_positive_status_json = conf.read_stream_positive_status_report_file()
    iwrefresh_status_json = conf.read_iw_refresh_status_report_file()
    job_list = conf.Read_job_list()
    job_stream_positive_test_report = conf.read_job_stream_positive_test_report()
    iw_refresh_positive_test_report = conf.read_iw_refresh_positive_test_report()


    def Append_job_status_to_report(self,test_type,job_status_dict):
        if test_type == 'jobstream_positive':
            file_name = self.job_positive_status_json
        else:
            file_name = ''
        with open(file_name,'r+') as f:
            file_lines = f.read()
            f.seek(0,0)
            if len(file_lines) != 0:
                file_json = json.loads(file_lines)              
                new_json_dict = dict()
                for k,v in file_json.items():
                    new_json_dict[k] = v
                for k,v in job_status_dict.items():
                    new_json_dict[k] = v
                f.write(json.dumps(new_json_dict))
            else:
                f.write(json.dumps(job_status_dict))

    def write_iwefresh_status_to_report(self,iw_refresh_report_json):
        file_name = self.iwrefresh_status_json
        with open(file_name,'r+') as f:
            json.dump(iw_refresh_report_json,f)

    def generate_jobstream_positive_report(self):
        file_name = self.job_positive_status_json
        job_positive_status_dict = dict()
        with open(file_name,'r+') as f:
            job_positive_status_dict = json.load(fp=f)
        print(job_positive_status_dict)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('job_stream_positive')
        ws.write(0,0,'JOB_NAME')
        ws.write(0,1,'JOB_TYPE')
        ws.write(0,2,'JOB_STATUS')
        ws.write(0,3,'START_TIME')
        ws.write(0,4,'END_TIME')
        rows = []
        for k in job_positive_status_dict:
            v = job_positive_status_dict[k]
            row = []
            job_name = k
            job_type = ''
            for job in self.job_list:
                if job['JOB_NAME'] == job_name:
                    job_type = job['JOB_TYPE']
            job_status = v['Job Status']
            start_time = v['Job Start Time']
            end_time = v['Last Run Time']
            row.append(job_name)
            row.append(job_type)
            row.append(job_status)
            row.append(start_time)
            row.append(end_time)
            rows.append(row)
        print(rows)
        for i in range(1,len(rows)+1):
            for j in range(5):
                ws.write(i,j,rows[i-1][j])
        saved_file_name = self.job_stream_positive_test_report
        wb.save(saved_file_name)

    def generate_iwrefresh_positive_report(self):
        file_name = self.iwrefresh_status_json
        iwrefresh_positive_report_dict = dict()
        with open(file_name,'r+') as f:
            iwrefresh_positive_report_dict = json.load(fp=f)
        print(iwrefresh_positive_report_dict)
        wb = xlwt.Workbook()
        ws = wb.add_sheet('iwrefresh_positive')
        ws.write(0,0,'JOB_NM')
        ws.write(0,1,'JOB_START_TIME')
        ws.write(0,2,'JOB_END_TIME')
        ws.write(0,3,'DATA_GROUP_NM')
        ws.write(0,4,'IWREFRESH_START_TIME')
        ws.write(0,5,'IWREFRESH_END_TIME')
        ws.write(0,6,'IWREFRESH_STATUS')
        ws.write(0,7,'TEST_STATUS')
        rows = []
        for item in iwrefresh_positive_report_dict:
            row = []
            row.append(item['JOB_NM'])
            row.append(item['JOB_START_TIME'])
            row.append(item['JOB_END_TIME'])
            row.append(item['DATA_GROUP_NM'])
            row.append(item['IWREFRESH_START_TIME'])
            row.append(item['IWREFRESH_END_TIME'])
            row.append(item['IWREFRESH_STATUS_'])
            row.append('PASS' if item['IWREFRESH_STATUS_'] == 'COMPLETE' else 'FAIL')
            rows.append(row)
        print(rows)
        for i in range(1,len(rows)+1):
            for j in range(8):
                ws.write(i,j,rows[i-1][j])
        saved_file_name = self.iw_refresh_positive_test_report
        wb.save(saved_file_name)





if __name__ == "__main__":
    Gen_report = Generate_report()
    Gen_report.generate_iwrefresh_positive_report()
