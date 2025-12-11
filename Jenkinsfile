pipeline {
    agent any
    
    options {
        skipDefaultCheckout true  // Отключаем автоматический checkout
        timeout(time: 30, unit: 'MINUTES')  // Ограничиваем время выполнения
    }
    
    stages {
        stage('Checkout') {
            steps {
                // ОДИН раз делаем checkout с таймаутом
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/pva-hw37']],
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Vladimir180791/pva-hw37.git'
                    ]]
                ])
            }
        }
        
        stage('Setup Environment') {
            steps {
                script {
                    // ПРОВЕРЯЕМ что установлено
                    sh 'python --version 2>&1 || echo "Python не найден"'
                    sh 'pip --version 2>&1 || echo "Pip не найден"'
                    
                    // Быстрая установка без venv (для скорости)
                    sh 'pip install --user --upgrade pip 2>&1'
                    sh 'pip install --user -r requirements.txt 2>&1'
                    
                    // ИЛИ с venv (если нужно изоляция)
                    // sh 'python -m venv venv --clear 2>&1'
                    // sh 'call venv\\Scripts\\activate.bat && pip install -r requirements.txt 2>&1'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                // Запускаем тесты с таймаутом
                sh 'python -m pytest tests/ -v --tb=short --html=reports/report.html --self-contained-html 2>&1'
                
                // ИЛИ если используете venv
                // sh 'call venv\\Scripts\\activate.bat && python -m pytest tests/ -v --tb=short --html=reports/report.html --self-contained-html 2>&1'
            }
        }
    }
    
    post {
        always {
            // Публикация отчета только если он существует
            script {
                def reportExists = fileExists 'reports/report.html'
                if (reportExists) {
                    publishHTML(target: [
                        reportDir: 'reports',
                        reportFiles: 'report.html',
                        reportName: 'Test Report'
                    ])
                }
            }
        }
    }
}