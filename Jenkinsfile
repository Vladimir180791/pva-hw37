pipeline {
    agent any
    
    environment {
        PYTHON_PATH = "${WORKSPACE}"
        ALLURE_RESULTS = "${WORKSPACE}/reports/allure-results"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                url: 'https://github.com/your-username/saucedemo-autotests.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                pytest tests/ \
                  --browser=chrome \
                  --headless \
                  --alluredir=${ALLURE_RESULTS} \
                  -v
                '''
            }
        }
        
        stage('Generate Report') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure-results']]
                    ])
                }
            }
        }
    }
    
    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports/html',
                reportFiles: 'report.html',
                reportName: 'HTML Report'
            ])
        }
    }
}