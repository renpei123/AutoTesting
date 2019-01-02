pipeline {
    agent any 
    stages {
        stage('Build') {
		      steps {
                bat 'C:/ProgramData/Anaconda3/python -m py_compile sources/DS_AutoTesting/Read_conf.py'
                bat 'C:/ProgramData/Anaconda3/python -m py_compile sources/DS_AutoTesting/test_engine.py'
                bat 'C:/ProgramData/Anaconda3/python -m py_compile sources/DS_AutoTesting/test_pre_action.py'
                bat 'C:/ProgramData/Anaconda3/python -m py_compile sources/DS_AutoTesting/Job_stream_test.py'
                bat 'C:/ProgramData/Anaconda3/python -m py_compile sources/DS_AutoTesting/DS_Operation.py'
    
            }
        }
		
		stage('Positive_Test_Pre_Action') { 
               steps {
                bat 'C:/ProgramData/Anaconda3/python sources/DS_AutoTesting/test_engine.py' 
            }
        }
    }
}