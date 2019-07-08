pipeline {
    agent any 
	
	parameters {
	string(name:'dspassword', defaultValue: 'dspassword', description: 'dataStage_password')
	string(name:'iwpassword', defaultValue: 'iwpassword', description: 'iwrefresh_password')
	}
	

    stages {
	
		
        stage('Build') {
		      steps {
				echo "the path of WORKSPACE is ${env.WORKSPACE}" 
                bat "python -m py_compile ${env.WORKSPACE}/sources/DS_AutoTesting/Read_conf.py"
                bat "python -m py_compile ${env.WORKSPACE}/sources/DS_AutoTesting/test_engine.py"
                bat "python -m py_compile ${env.WORKSPACE}/sources/DS_AutoTesting/test_pre_action.py"
                bat "python -m py_compile ${env.WORKSPACE}/sources/DS_AutoTesting/Job_stream_test.py"
                bat "python -m py_compile ${env.WORKSPACE}/sources/DS_AutoTesting/DS_Operation.py"
    
            }
        }
		
		stage('Positive_Test_Pre_Action') { 
               steps {
                bat "python ${env.WORKSPACE}/sources/DS_AutoTesting/test_engine.py positive_test_pre_action dsdev params.dspassword"
            }
        }
		
		stage('Job_stream_test') { 
               steps {
                bat "python ${env.WORKSPACE}/sources/DS_AutoTesting/test_engine.py job_stream_test positive dsdev params.dspassword"
            }
        }
		
		stage('IW_Refresh_Test') { 
               steps {
                bat "python ${env.WORKSPACE}/sources/DS_AutoTesting/test_engine.py iw_refresh_test positive siwwebd params.iwpassword" 
            }
        }
    }
}