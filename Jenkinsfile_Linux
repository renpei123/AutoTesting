pipeline {
    agent any
    stages {
        stage('Build') {
		steps {
				sh 'python'
                sh 'python -m py_compile sources/Sample_SSH.py' 
            }
        }
				
	stage('JobStreamTest') { 
         steps {
				sh 'echo "Job Stream Test started"'
                sh 'python sources/Job_Steam_Test.py' 
            }
        }
	stage('ASCATest') { 
               steps {
                sh 'echo "ASCA Control Test started"'
				sh 'python sources/ASCA_Control_Test.py' 
            }
        }
	stage('IWControlTest') { 
               steps {
                sh 'echo "IW Control Test started"'
                sh 'python sources/IW_Control_Test.py' 
            }
        }
	stage('DataAccuracy') { 
              steps {
               sh 'echo "Data Accuracy Test started"'
               sh 'python sources/Data_Accuracy_Test.py' 
           }
       }	
    }
}