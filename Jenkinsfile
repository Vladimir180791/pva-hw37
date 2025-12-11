pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['development', 'staging', 'production'], description: 'Test environment')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser for tests')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        string(name: 'BASE_URL', defaultValue: 'https://www.saucedemo.com', description: 'Application URL')
        string(name: 'PARALLEL_WORKERS', defaultValue: '2', description: 'Number of parallel workers')
    }
    
    environment {
        ENVIRONMENT = "${params.ENVIRONMENT}"
        BROWSER = "${params.BROWSER}"
        HEADLESS = "${params.HEADLESS}"
        BASE_URL = "${params.BASE_URL}"
        PARALLEL_WORKERS = "${params.PARALLEL_WORKERS}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                // Для Windows используем checkout без sh
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/pva-hw37']],
                    userRemoteConfigs: [[url: 'https://github.com/Vladimir180791/pva-hw37.git']],
                    extensions: [[$class: 'CleanBeforeCheckout']]
                ])
            }
        }
        
        stage('Setup Environment') {
            steps {
                // НА WINDOWS ИСПОЛЬЗУЕМ bat ВМЕСТО sh!
                bat """
                    echo "=== НАСТРОЙКА ОКРУЖЕНИЯ ДЛЯ WINDOWS ==="
                    echo "Окружение: %ENVIRONMENT%"
                    echo "Браузер: %BROWSER%"
                    echo "Headless: %HEADLESS%"
                    echo "Base URL: %BASE_URL%"
                    echo "Параллельных воркеров: %PARALLEL_WORKERS%"
                """
                
                // Создаем .env файл для Python
                bat """
                    echo Создаем .env файл с настройками...
                    (
                        echo ENVIRONMENT=%ENVIRONMENT%
                        echo BROWSER=%BROWSER%
                        echo HEADLESS=%HEADLESS%
                        echo BASE_URL=%BASE_URL%
                        echo STANDARD_USER=standard_user
                        echo STANDARD_PASSWORD=secret_sauce
                        echo TIMEOUT=10
                        echo PAGE_LOAD_TIMEOUT=30
                        echo GENERATE_ALLURE=true
                        echo GENERATE_HTML=true
                        echo SAVE_SCREENSHOTS=on_failure
                        echo PARALLEL_WORKERS=%PARALLEL_WORKERS%
                    ) > .env
                    
                    echo Содержимое .env:
                    type .env
                """
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat """
                    echo "=== УСТАНОВКА ЗАВИСИМОСТЕЙ ==="
                    
                    echo Проверяем Python...
                    python --version || echo "Python не найден, проверьте PATH"
                    
                    echo Обновляем pip...
                    python -m pip install --upgrade pip
                    
                    echo Устанавливаем зависимости из requirements.txt...
                    if exist requirements.txt (
                        pip install -r requirements.txt
                    ) else (
                        echo "requirements.txt не найден, устанавливаем базовые зависимости"
                        pip install selenium webdriver-manager pytest pytest-html allure-pytest pytest-xdist python-dotenv
                    )
                    
                    echo "=== УСТАНОВКА ДЛЯ WINDOWS ==="
                    pip install pywin32  # Для работы с Windows
                    
                    echo Список установленных пакетов:
                    pip list
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                bat """
                    echo "=== ЗАПУСК ТЕСТОВ ==="
                    
                    echo Создаем директории для отчетов...
                    if not exist reports mkdir reports
                    if not exist reports\\allure-results mkdir reports\\allure-results
                    if not exist reports\\html mkdir reports\\html
                    
                    echo Запускаем тесты с параметрами...
                    python -m pytest tests/ ^
                        --junitxml=reports\\junit.xml ^
                        --html=reports\\html\\report.html ^
                        --self-contained-html ^
                        -n %PARALLEL_WORKERS% ^
                        --timeout=300 ^
                        -v
                    
                    echo Код завершения тестов: %ERRORLEVEL%
                """
            }
            
            post {
                always {
                    // Сохраняем артефакты независимо от результата
                    archiveArtifacts artifacts: 'reports\\**\\*', fingerprint: true
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                bat """
                    echo "=== ГЕНЕРАЦИЯ ОТЧЕТОВ ==="
                    
                    echo Проверяем наличие Allure...
                    allure --version 2>nul || (
                        echo "Allure не установлен в системе"
                        echo "Устанавливаем через npm..."
                        npm install -g allure-commandline 2>nul || echo "npm не доступен"
                    )
                    
                    echo Генерируем Allure отчет если есть результаты...
                    if exist reports\\allure-results\\*.json (
                        echo Найдены результаты Allure, генерируем отчет...
                        allure generate reports\\allure-results -o reports\\allure-report --clean
                    ) else (
                        echo "Результаты Allure не найдены"
                    )
                    
                    echo "=== ГОТОВЫЕ ОТЧЕТЫ ==="
                    dir reports /s
                """
            }
        }
    }
    
    post {
        always {
            // Публикация HTML отчета
            publishHTML(target: [
                reportDir: 'reports/html',
                reportFiles: 'report.html',
                reportName: 'HTML Test Report',
                keepAll: true
            ])
            
            // Очистка
            bat """
                echo "=== ОЧИСТКА ==="
                echo Удаляем временные файлы...
                del .env 2>nul
                echo Готово!
            """
        }
        
        success {
            echo "✅ ТЕСТЫ УСПЕШНО ЗАВЕРШЕНЫ!"
            // Можно добавить уведомление в Teams/Slack
        }
        
        failure {
            echo "❌ ТЕСТЫ ЗАВЕРШИЛИСЬ С ОШИБКОЙ!"
            // Можно добавить уведомление об ошибке
        }
    }
}