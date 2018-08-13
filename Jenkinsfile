pipeline {
    agent any 
    stages {
        stage('Build') {
             agent { docker }

		steps {
		sh 'python'
                sh 'python -m py_compile sources/RDM_JobStream_Test.py' 
            }
        }
		
		
	stage('Test') { 
	    agent { docker }
               steps {
                sh 'python sources/RDM_JobStream_Test.py' 
            }
        }
    }
}