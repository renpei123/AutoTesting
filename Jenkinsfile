pipeline {
    agent any 
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