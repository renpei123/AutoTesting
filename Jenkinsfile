pipeline {
    agent none 
    stages {
        stage('Build') {
		agent none
            steps {
                bat 'python -m py_compile sources/RDM_JobStream_Test.py' 
            }
        }
		
		stage('Test') { 
            agent  none
            steps {
                bat 'python sources/RDM_JobStream_Test.py' 
            }
        }
    }
}