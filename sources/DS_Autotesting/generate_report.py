# -*- coding: utf-8 -*-
import json
from Read_conf import ReadConfig
"""
Created on Fri Jan 18 17:59:57 2019

@author: RongHe
"""

class Generate_report:
    conf = ReadConfig()
    job_positive_status_report = conf.read_stream_positive_status_report_file()
    iwrefresh_status_report = conf.read_iw_refresh_status_report_file()

    def Append_job_status_to_report(self,test_type,job_status_dict):
        if test_type == 'jobstream_positive':
            file_name = self.job_positive_status_report
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
        file_name = self.iwrefresh_status_report
        with open(file_name,'r+') as f:
            json.dump(iw_refresh_report_json,f)



if __name__ == "__main__":   
    pass
