pipeline {
    agent any 
    stages {
        stage('Build') {
             agent { docker image 'python:3.6' }

		steps {
		sh 'python'
                sh 'python -m py_compile sources/RDM_JobStream_Test.py' 
            }
        }
		
		
	stage('Test') { 
	    agent {  docker image 'python:3.6' }
               steps {
                sh 'python sources/RDM_JobStream_Test.py' 
            }
        }
    }
}