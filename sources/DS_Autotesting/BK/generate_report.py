# -*- coding: utf-8 -*-
import json

"""
Created on Fri Jan 18 17:59:57 2019

@author: RongHe
"""

class Generate_report:
    job_positive_status_report = 'tmp/job_status_report.json'
    
    
    def Append_job_status(self,test_type,job_status_dict):
        if test_type == 'jobstream_positive':
            
            file_name = self.job_positive_status_report
            #json_str = json.dumps(job_status_dict)
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
if __name__ == "__main__":   
    pass
    