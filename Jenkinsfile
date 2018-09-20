pipeline {
    agent any 
    stages {
        stage('Build') {
		steps {
				sh 'python'
                sh 'python -m py_compile sources/Sample_SSH.py' 
            }
        }

    }
}