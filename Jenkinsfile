pipeline {
    agent none 
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:2-alpine' 
                }
            }
            steps {
                sh 'python -m py_compile sources/RDM_JobStream_Test.py' 
            }
        }
		
		stage('Test') { 
            agent {
                docker {
                    image 'python:2-alpine' 
                }
            }
            steps {
                sh 'python sources/RDM_JobStream_Test.py' 
            }
        }
    }
}