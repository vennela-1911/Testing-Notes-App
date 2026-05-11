pipeline {

    agent any

    options {
        timestamps()
        timeout(time: 1, unit: 'HOURS')
    }

    environment {
        PYTHONUNBUFFERED = "1"
    }

    stages {

        stage('Checkout SCM') {
            steps {
                git branch: 'main',
                url: 'https://github.com/vennela-1911/Testing-Notes-App.git'
            }
        }

        stage('Verify Python') {
            steps {
                bat '''
                python --version
                python -m pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m pip install --upgrade pip
                python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Clean Workspace') {
            steps {
                bat '''
                if exist allure-results rmdir /s /q allure-results
                mkdir allure-results
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                python -m pytest tests/api -v --alluredir=allure-results
                '''
            }
        }

        stage('Run UI Tests') {
            steps {
                bat '''
                python -m pytest tests/ui -v ^
                --reruns 1 ^
                --reruns-delay 2 ^
                --alluredir=allure-results
                '''
            }
        }

        stage('Run AI Tests') {
            steps {
                bat '''
                python -m pytest tests/ai -v --alluredir=allure-results
                '''
            }
        }

        stage('Run E2E Tests') {
            steps {
                bat '''
                python -m pytest tests/e2e -v --alluredir=allure-results
                '''
            }
        }
    }

    post {

        always {

            archiveArtifacts artifacts: 'allure-results/**/*.*', allowEmptyArchive: true

            junit allowEmptyResults: true,
            testResults: '**/pytest.xml'
        }

        success {
            echo 'SUCCESS: All 18 test cases passed.'
        }

        failure {
            echo 'FAILURE: Pipeline failed.'
        }
    }
}
