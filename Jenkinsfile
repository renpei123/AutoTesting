pipeline {
    agent any 
    stages {
        stage('Build') {
             agent { docker image 'python'}

		steps {
		sh 'python'
                sh 'python -m py_compile sources/RDM_JobStream_Test.py' 
            }
        }
		
		
	stage('Test') { 
	    agent { agent { docker image 'python'} }
               steps {
                sh 'python sources/RDM_JobStream_Test.py' 
            }
        }
    }
}