pipeline {
    agent any
    
    // Отключаем автоматический checkout чтобы избежать дублирования
    options {
        skipDefaultCheckout true
        timeout(time: 15, unit: 'MINUTES')
    }
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['development', 'staging', 'production'], description: 'Test environment')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser for tests')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        string(name: 'BASE_URL', defaultValue: 'https://www.saucedemo.com', description: 'Application URL')
        string(name: 'PARALLEL_WORKERS', defaultValue: '2', description: 'Number of parallel workers')
    }
    
    stages {
        stage('Checkout') {
            steps {
                // ОДИН checkout, простой
                checkout scm
                
                // Проверяем что файлы есть
                bat """
                    echo === ПРОВЕРКА ФАЙЛОВ ===
                    dir /b
                    if exist requirements.txt echo requirements.txt найден
                """
            }
        }
        
        stage('Setup Environment') {
            steps {
                // Используем простой bat с минимальными echo
                bat """
                    echo === НАСТРОЙКА ОКРУЖЕНИЯ ===
                    echo Окружение: %ENVIRONMENT%
                    echo Браузер: %BROWSER%
                    echo Headless: %HEADLESS%
                    
                    rem Создаем .env файл БЕЗ сложных символов
                    (
echo BASE_URL=https://www.saucedemo.com
echo STANDARD_USER=standard_user
echo STANDARD_PASSWORD=secret_sauce
echo TIMEOUT=10
                    ) > test_env.txt
                    
                    type test_env.txt
                """
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat """
                    echo === УСТАНОВКА ЗАВИСИМОСТЕЙ ===
                    
                    echo Проверяем Python:
                    python --version
                    if errorlevel 1 exit 1
                    
                    echo Устанавливаем минимальные зависимости:
                    pip install selenium webdriver-manager pytest
                    
                    echo Проверяем установку:
                    pip list | findstr /i "selenium pytest"
                """
            }
        }
        
        stage('Run Simple Test') {
            steps {
                bat """
                    echo === ЗАПУСК ПРОСТОГО ТЕСТА ===
                    
                    rem Создаем простой тест для проверки
                    echo import pytest > test_simple.py
                    echo def test_one(): >> test_simple.py
                    echo     assert 1 == 1 >> test_simple.py
                    
                    rem Запускаем тест
                    python -m pytest test_simple.py -v
                    
                    rem Очищаем
                    del test_simple.py 2>nul
                """
            }
        }
        
        stage('Run Real Tests') {
            when {
                expression { return true }
            }
            steps {
                bat """
                    echo === ЗАПУСК РЕАЛЬНЫХ ТЕСТОВ ===
                    
                    rem Создаем папки для отчетов
                    if not exist reports mkdir reports
                    if not exist reports\\html mkdir reports\\html
                    
                    rem Запускаем тесты
                    echo Запускаем тест логина...
                    python -m pytest tests/test_login.py -v --tb=short --html=reports\\html\\report.html --self-contained-html
                    
                    echo Код завершения: %ERRORLEVEL%
                """
            }
        }
    }
    
    post {
        always {
            // Сохраняем отчеты если они есть
            script {
                try {
                    if (fileExists('reports/html/report.html')) {
                        archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
                        
                        publishHTML(target: [
                            reportDir: 'reports/html',
                            reportFiles: 'report.html',
                            reportName: 'Test Report',
                            keepAll: true
                        ])
                    }
                } catch (Exception e) {
                    echo "Ошибка при сохранении отчетов: ${e}"
                }
            }
            
            // Очистка через простой bat
            bat """
                echo === ОЧИСТКА ===
                del test_env.txt 2>nul
                echo Готово
            """
        }
        
        success {
            echo "ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО"
        }
        
        failure {
            echo "ТЕСТЫ ЗАВЕРШИЛИСЬ С ОШИБКОЙ"
        }
    }
}