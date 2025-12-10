pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                // ВМЕСТО sh используйте bat для Windows
                bat 'python -m venv venv'
                bat 'call venv\\Scripts\\activate.bat'
                bat 'pip install -r requirements.txt'
                
                // Если нужно установить ChromeDriver
                bat 'pip install webdriver-manager'
            }
        }
        
        stage('Run Tests') {
            steps {
                // Для запуска тестов
                bat 'pytest tests/ --html=reports/html/report.html --self-contained-html'
                // или если используете скрипт
                bat 'python run_tests.py'
            }
        }
        
        stage('Generate Report') {
            steps {
                // Копирование или обработка отчетов
                bat 'copy reports\\html\\*.html %WORKSPACE%\\reports\\'  // Пример для Windows
            }
        }

        stage('Diagnostics') {
            steps {
                bat 'where python'
                bat 'python --version'
                bat 'where git'
                bat 'echo %WORKSPACE%'
            }
        }
    }
    
    post {
        always {
            // Публикация HTML отчета (это Jenkins плагин, не команда)
            publishHTML(target: [
                reportDir: 'reports/html',
                reportFiles: 'report.html',
                reportName: 'HTML Report'
            ])
        }
    }
}