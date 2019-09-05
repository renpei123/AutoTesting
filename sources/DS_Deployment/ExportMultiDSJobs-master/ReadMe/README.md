# Source code structure
- export_ds.py
- conf
  - conf.ini
  - job_list.ini

# How to run
1. edit conf.ini by entering your server, project, user, password, etc. information
2. run export_ds.py on commandline
- list jobs - list all job names and store into conf/job_list file
```
python export_ds.py list
```
- export - export all the jobs into dsx files start from exported number in the conf file, we can start from where we stopped
```
python export_ds.py export
```
- organize jobs into folders
```
python export_ds.py categorize
```
