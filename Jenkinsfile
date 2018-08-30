pipeline {
    agent { 
		docker { image 'ubuntu-with-autotesting:latest' }
			 }
    stages {
        stage('Build') {
		steps {
				sh 'python'
                sh 'python -m py_compile sources/Sample_SSH.py' 
            }
        }
				
	stage('Remote_Connection') { 
               steps {
                sh 'python sources/Sample_SSH.py' 
            }
        }
    }
}