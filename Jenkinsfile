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

        stage('Install Dependencies') {
            steps {
                bat '''
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Clean Workspace') {
            steps {
                bat '''
                if exist allure-results rmdir /s /q allure-results
                mkdir allure-results

                if exist reports rmdir /s /q reports
                mkdir reports
                '''
            }
        }

        stage('Run API Tests') {
            steps {
                bat '''
                pytest tests/api -v --alluredir=allure-results
                '''
            }
        }

        stage('Run UI Tests') {
            steps {
                bat '''
                pytest tests/ui -v --alluredir=allure-results
                '''
            }
        }

        stage('Run AI Tests') {
            steps {
                bat '''
                pytest tests/ai -v --alluredir=allure-results
                '''
            }
        }
    }

    post {

        always {

            archiveArtifacts artifacts: 'reports/**/*.*', allowEmptyArchive: true

            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }

        success {
            echo 'Pipeline executed successfully.'
        }

        failure {
            echo 'Pipeline execution failed.'
        }
    }
}
