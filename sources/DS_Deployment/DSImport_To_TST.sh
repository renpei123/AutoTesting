#!/bin/bash
##########################################################################################################
# Author: Siva S                                                                                         #
# Since: 2017-10-29                                                                                      #                          
# Description: This script pulls the code corresponding to a Git tag and imports it to datastage server. #
##########################################################################################################
#if [ $# -ge 2 || $# -lt 1 ]
#then
#    echo 'Invalid number of arguments. Please correct and rerun the script'
#	exit 1
#fi
pcrref=$1
repopath='/gmudata/GDDM_Git/MagicHat/GDDM'
#repopath=$2
sql_flg=$3
archpath='/gmudata/DEPLOY'
now=$(date '+%Y%m%d%H%M%s')
basetagnm="$(echo $pcrref | cut -d'_' -f1)"
#mkdir $archpath/$pcrref"_"$now
cd $repopath
git pull origin master
if [ $? -eq 0 ]
then
  echo "pull was successful"
else
  echo "MERGE CONFLICTS Needs to be fixed";
  git add -A;
  git commit -m"to resolve conflicts";
  git pull origin master;
fi
if [ "$2" = "Y" ];
 then
git fetch --all --tags --prune
git checkout "tags/"$pcrref
git log --reverse --pretty=oneline --name-only --grep=$pcrref --format="%h" | grep "dsx" | uniq > $archpath/$pcrref"_"$now"_"dsx".lst"
var=0
for dsx in `cat $archpath/$pcrref"_"$now"_"dsx".lst"`
do
	var=$((var+1))
	echo "$dsx"" is ready to get imported"
	/opt/IBM/InformationServer11/ASBNode/bin/DSXImportService.sh -ISFile /gmudata/SIWB_AuthFile.txt -DSHost SIWB:31539 -DSProject TST_IMGDM -DSXFile $repopath"/"$dsx -Overwrite >> $archpath/$pcrref"_"$now"_"dsx".log"
	echo "$dsx"" has been imported"
done
else
  echo "datastage deployment flag has not been selected hence it will be skipped"
fi

if [ "$3" = "Y" ];
 then
   echo "SQL flag selected. Ready to execute ddl or dml files in db2, netezza"
  git pull origin master
if [ $? -eq 0 ]
then
  echo "pull was successful"
else
  echo "MERGE CONFLICTS Needs to be fixed";
  git add -A;
  git commit -m"to resolve conflicts";
  git pull origin master;
fi
   git log --reverse --pretty=oneline --name-only --grep=$pcrref --format="%h" | grep ".sql" | grep "DB2" | uniq > $archpath/$pcrref"_"$now"_"db2sql".lst"
   git log --reverse --pretty=oneline --name-only --grep=$pcrref --format="%h" | grep ".sql" | grep "Netezza" | uniq > $archpath/$pcrref"_"$now"_"nzsql".lst"
db2 connect to gmudbdev user sseemaku using ********;    
for db2sql in `cat $archpath/$pcrref"_"$now"_"db2sql".lst"`
     do
      var=$((var+1))
      echo "$db2sql"" is ready to be executed"
     db2 -tvf $repopath"/"$db2sql > $archpath/$pcrref"_"$now"_"db2sql".log"
if [ $? -eq 0 ]
then
   echo "$db2sql"" has been executed successfully"
else
  echo "$db2sql"" has failed, please check the log"
fi
done	
db2 terminate;
  for nzsql in `cat $archpath/$pcrref"_"$now"_"nzsql".lst"`
    do
      var=$((var+1))
      echo "$nzsql"" is ready to be executed"
	 #db2 -tvf
      echo "$nzsql"" has been executed"
   done
else 
  echo "SQL flag not selected. Database import is skipped"
fi
if [ "$4" = "Y" ];
 then
   echo "Unix flag selected"
  git pull origin master
if [ $? -eq 0 ]
then
  echo "pull was successful"
else
  echo "MERGE CONFLICTS Needs to be fixed";
  git add -A;
  git commit -m"to resolve conflicts";
  git pull origin master;
fi
   git log --reverse --pretty=oneline --name-only --grep=$pcrref --format="%h" | grep "Unix" | uniq > $archpath/$pcrref"_"$now"_"Unix".lst"
for unix_file in `cat $archpath/$pcrref"_"$now"_"Unix".lst"`
     do
      var=$((var+1))
      echo "$unix_file"" is ready to be copied"
     #db2 -tvf $repopath"/"$db2sql > $archpath/$pcrref"_"$now"_"db2sql".log"
  cp $repopath"/"$unix_file /DS_Data/gmu/TST/IMGDM/control/
echo "$repopath"/"$unix_file /DS_Data/gmu/TST/IMGDM/control/"
if [ $? -eq 0 ]
then
   echo "$unix_file"" has been copied successfully"
else
  echo "$unix_file"" file copy failed, please check the log"
fi
done
else 
  echo "Unix file deployment skipped"
fi
