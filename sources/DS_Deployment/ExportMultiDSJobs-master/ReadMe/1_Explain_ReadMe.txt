 1st step: configure the conf.ini file based on your server info.

  Domain: DS engine server, in host name.
  Host: DS information server, in Project.
  jobs_dir: It's the job export local path .
  Command_Path: It's the installation path, but use the slash in python,C:/IBM/InformationServer/  it's backslash in windows. C:\IBM\InformationServer\

 2nd step: check the python installation, include the regex module.

 how to check regex module: go to link :   C:\Users\YAHUANG\AppData\Local\Programs\Python\Python36
  For me, use the pip command to install regex module. first find the pip.exe path, and cd C:\Users\YAHUANG\AppData\Local\Programs\Python\Python36\Scripts
  Run the command: C:\Users\YAHUANG\AppData\Local\Programs\Python\Python36\Scripts>pip install regex

 3rd step: After installation succeed, locate the path to python script directory, run the following command to execute the python script.
  C:\Users\YAHUANG\Desktop\DS\Load job function\5_Alex_ExportMultiDSJobs-master>python export_ds.py list
  It's the result: Status code = 0
  It means the exported successfully. all job list in the conf\job_list.
 comment: if you write wrong project, you will get the following error message:
   Status code = -1002 DSJE_BADPROJECT

 4th step: First change the directory in python script line 67 to your actual confi.ini file path. Then execute the export job steps.
  C:\Users\YAHUANG\Desktop\DS\Load job function\5_Alex_ExportMultiDSJobs-master>python export_ds.py export


 5th step: To execute the organizion of job folder. 
 C:\Users\YAHUANG\Desktop\DS\Load job function\5_Alex_ExportMultiDSJobs-master>python export_ds.py categorize
  All job will copy to (not move to, can be optimized) jobs_dir directory defined in confi.ini.

 6th step: To execute the organizion of job folder. 
 export=0 means: we load data from the job list num 1, everytime we must set it to defaut value(0)


 ------For RDF------

[host]
host = RDTST1ER:31539
domain = rdtst1er.sby.ibm.com:9080
user = yanged
password = Temp4you
project = ActaMigration

[dir]
jobs_dir = C:/Users/IBM_ADMIN/Desktop/WWPRT/3_RDF/00_01_RDF_Overview/3_All_Job_List_201801
job_list_file = conf/job_list
exported = 0

[sys]
command_path = C:/IBM/InformationServer/Clients/Classic/


 ------For WWPRTDEV2------

[host]
host = zdsdeveng02
domain = zdsdevdom02:443
user = huangycd
password = kiki201801
project = WWPRT_Dry_Run

[dir]
jobs_dir = C:/Users/YAHUANG/Desktop/RDF/JP/JP_MIG_JOBS
job_list_file = conf/job_list
exported = 0

[sys]
command_path = C:/IBM/InformationServer/Clients/Classic/

