#!/bin/bash
# Author: Wei E Lu/China/IBM
# Since: 2017-08-08
# Description: Delpoy latest shell and DS jobs from Jenkins to Pre-Prod DS_SERVER.
# Changes: 1. Add MQ BAR file deploy 2017-08-18
#

# Define ENV;
WORKSPACE=/var/lib/jenkins/workspace/RDF_Pre-Prod
CUR_DATE=$(date +%Y%m%d%H%M)
USER=cn212995
PASSWD=password
CHANGELIST=$WORKSPACE/changelist_$CUR_DATE.txt
DS_SERVER=xxx
DS_SERVER_TAG=tag
DS_SERVER_SHORT_NAME=user
DS_SERVER_SU_USER=user
MQ_SERVER=xxx
MQ_SERVER_TAG=tag
MQ_SERVER_SHORT_NAME=user
MQ_SERVER_SU_USER=user
MQ_SERVER_SU_GROUP=user
MQ_BARFILE=bafile.bar
MQ_NAME=mqname
MQ_NAME_Broker=wss2rdf_Broker
EAR_FILE=RDFinanceEAR.ear
EAR_SERVER=xxx
EAR_SERVER_SU_USER=user
EAR_FOLDER=/usr/WebSphere85_kr3es/AppServer/profiles/AppServer/installedApps
EAR_BIN_FOLDER=/usr/WebSphere85_kr3es/AppServer/profiles/Dmgr/bin

# 1. Get change list from GIT SERVER;
# 2. Save chagne list to changelist.txt;
#git log -3 --name-only --oneline
#git log --committer 'yanged' --grep 'A rate' --oneline --name-only > $CHANGELIST
git log --grep 'B370' --oneline --name-only > $CHANGELIST
#git log -5 --committer 'fqzhang' --grep 'fix' --oneline --name-only > $CHANGELIST

chmod -R u=rwx,g=rx,o=r $WORKSPACE

cat $CHANGELIST
exit 0;

# Read from change list file
for file in $(cat $CHANGELIST)
    do
        # Read shell script and upload to DS_SERVER.
        if [[ $file =~ (\.sh)$ ]]; then
            echo Find new shell file: $WORKSPACE/$file, ready to deploy to $DS_SERVER 
            F_NAME=${file##*/}
            expect << EOT
            #set timeout 50
            spawn scp -r $WORKSPACE/$file $USER@$DS_SERVER:/auto/home/$USER/
            expect "(yes/no)?" {send "yes\r"}
            expect "password:" {send "$PASSWD\r"}
            expect EOT
            spawn ssh $USER@$DS_SERVER
            expect "(yes/no)?" {send "yes\r"}
            expect "password:" {send "$PASSWD\r"}
            expect "$DS_SERVER_TAG:/auto/home/$USER $ " {send "chmod u=rwx,g=rx,o=r /auto/home/$USER/$F_NAME\r"}
            expect "$DS_SERVER_TAG:/auto/home/$USER $ " {send "sudo su - $DS_SERVER_SU_USER\r"}
            expect "password:" {send "$PASSWD\r"}
            expect "$DS_SERVER_SU_USER@$DS_SERVER_TAG:/opt/IBM/InformationServer/Server/DSEngine $ " {send "cp -f /auto/home/$USER/$F_NAME /is/dsproj/ActaMigrationRepo/bin\r"}
            exec sleep 10
            expect "$DS_SERVER_SU_USER@$DS_SERVER_TAG:/opt/IBM/InformationServer/Server/DSEngine $ " {send "chmod u=rwx,g=rx,o=rx /is/dsproj/ActaMigrationRepo/bin/$F_NAME\r"}
            #expect "$DS_SERVER_SU_USER@$DS_SERVER_TAG:/opt/IBM/InformationServer/Server/DSEngine $ " {send "ls -l\r"}
            expect EOT
EOT
        # Read Datastage jobs and upload to DS_SERVER then import to Datastage project.
        elif [[ $file =~ (\.dsx)$ ]]; then
            echo Find new Datastage file: $WORKSPACE/$file, ready to deploy to $DS_SERVER 
            F_NAME=${file##*/}
            expect << EOT
            #set timeout 120
            spawn scp -r $WORKSPACE/$file $USER@$DS_SERVER:/auto/home/$USER/
            expect "password:" {send "$PASSWD\r"}
            expect EOT
            spawn ssh $USER@$DS_SERVER
            expect "(yes/no)?" {send "yes\r"}
            expect "password:" {send "$PASSWD\r"}
            expect "$DS_SERVER_TAG:/auto/home/$USER $ " {send "chmod u=rwx,g=rx,o=r /auto/home/$USER/$F_NAME\r"}
            expect "$DS_SERVER_TAG:/auto/home/$USER $ " {send "/opt/IBM/InformationServer/ASBNode/bin/DSXImportService.sh -ISFile /auto/home/$USER/DSConInfo.pas -DSHost $DS_SERVER_SHORT_NAME:xxx -DSProject xxx -DSXFile /auto/home/$USER/$F_NAME -Overwrite \r"} 
            exec sleep 20
            expect EOT
EOT
# Read conf file and upload to DS_SERVER.
        elif [[ $file =~ (\.conf)$ ]]; then
            echo Find new conf file: $WORKSPACE/$file, ready to deploy to $DS_SERVER 
            F_NAME=${file##*/}
            expect << EOT
            #set timeout 50
            spawn scp -r $WORKSPACE/$file $USER@$DS_SERVER:/auto/home/$USER/
            expect "(yes/no)?" {send "yes\r"}
            expect "password:" {send "$PASSWD\r"}
            expect EOT
            spawn ssh $USER@$DS_SERVER
            expect "(yes/no)?" {send "yes\r"}
            expect "password:" {send "$PASSWD\r"}
            expect "$DS_SERVER_TAG:/auto/home/$USER $ " {send "chmod u=rwx,g=rx,o=r /auto/home/$USER/$F_NAME\r"}
            expect "$DS_SERVER_TAG:/auto/home/$USER $ " {send "sudo su - $DS_SERVER_SU_USER\r"}
            expect "password:" {send "$PASSWD\r"}
            expect "$DS_SERVER_SU_USER@$DS_SERVER_TAG:/opt/IBM/InformationServer/Server/DSEngine $ " {send "cp -f /auto/home/$USER/$F_NAME /is/dsproj/ActaMigrationRepo/conf\r"}
            exec sleep 10
            expect "$DS_SERVER_SU_USER@$DS_SERVER_TAG:/opt/IBM/InformationServer/Server/DSEngine $ " {send "chmod u=rwx,g=rx,o=rx /is/dsproj/ActaMigrationRepo/conf/$F_NAME\r"}
            #expect "$DS_SERVER_SU_USER@$DS_SERVER_TAG:/opt/IBM/InformationServer/Server/DSEngine $ " {send "ls -l\r"}
            expect EOT
EOT
        else
            continue
        fi
    done