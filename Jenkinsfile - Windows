pipeline {
    agent any 
    stages {
        stage('Build') {
		      steps {
                bat 'python -m py_compile sources/RDM_JobStream_Test.py' 
            }
        }
		
		stage('Test') { 
               steps {
                bat 'python sources/RDM_JobStream_Test.py' 
            }
        }
    }
}