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
                python --version

                python -m pip install --upgrade pip

                python -m pip install -r requirements.txt

                python -m pip install webdriver-manager

                python -m pip install pytest-xdist

                python -m pip install allure-pytest
                '''
            }
        }

        stage('Clean Workspace') {

            steps {

                bat '''
                if exist allure-results rmdir /s /q allure-results

                if exist reports rmdir /s /q reports

                mkdir allure-results

                mkdir reports
                '''
            }
        }

        stage('Run API Tests') {

            steps {

                bat '''
                python -m pytest tests/api -v ^
                --alluredir=allure-results
                '''
            }
        }

        stage('Run UI Tests') {

            steps {

                bat '''
                python -m pytest tests/ui -n 2 -v ^
                --alluredir=allure-results
                '''
            }
        }

        stage('Run AI Tests') {

            steps {

                bat '''
                python -m pytest tests/ai -v ^
                --alluredir=allure-results
                '''
            }
        }

        stage('Run E2E Tests') {

            steps {

                bat '''
                python -m pytest tests/e2e -v ^
                --alluredir=allure-results
                '''
            }
        }
    }

    post {

        always {

            archiveArtifacts(
                artifacts: 'reports/**/*.*',
                allowEmptyArchive: true
            )

            allure([
                includeProperties: false,
                jdk: '',
                results: [[path: 'allure-results']]
            ])
        }

        success {

            echo 'All 18 test cases passed successfully.'
        }

        failure {

            echo 'Pipeline execution failed.'
        }
    }
}
