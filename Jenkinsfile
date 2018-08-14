pipeline {
    agent { 
		docker { image 'python:3.6' }
			 }
    stages {
        stage('Build') {
		steps {
		sh 'python'
                sh 'python -m py_compile sources/RDM_JobStream_Test.py' 
            }
        }
				
	stage('Test') { 
               steps {
                sh 'python sources/RDM_JobStream_Test.py' 
            }
        }
    }
}