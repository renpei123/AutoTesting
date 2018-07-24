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
                bat 'python -m py_compile sources/max_min.py sources/hello.py' 
            }
        }
    }
}