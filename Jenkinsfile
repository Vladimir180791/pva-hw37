pipeline {
    agent any
    
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
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                powershell '''
                    Write-Host "=== НАСТРОЙКА ОКРУЖЕНИЯ ДЛЯ WINDOWS ==="
                    Write-Host "Окружение: $env:ENVIRONMENT"
                    Write-Host "Браузер: $env:BROWSER"
                    Write-Host "Headless: $env:HEADLESS"
                    Write-Host "Base URL: $env:BASE_URL"
                    Write-Host "Параллельных воркеров: $env:PARALLEL_WORKERS"
                    
                    # Создаем .env файл
                    $envContent = @"
ENVIRONMENT=$env:ENVIRONMENT
BROWSER=$env:BROWSER
HEADLESS=$env:HEADLESS
BASE_URL=$env:BASE_URL
STANDARD_USER=standard_user
STANDARD_PASSWORD=secret_sauce
TIMEOUT=10
PAGE_LOAD_TIMEOUT=30
GENERATE_ALLURE=true
GENERATE_HTML=true
SAVE_SCREENSHOTS=on_failure
PARALLEL_WORKERS=$env:PARALLEL_WORKERS
"@
                    
                    $envContent | Out-File -FilePath .env -Encoding UTF8
                    Write-Host "Содержимое .env:"
                    Get-Content .env
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                powershell '''
                    Write-Host "=== УСТАНОВКА ЗАВИСИМОСТЕЙ ==="
                    
                    Write-Host "Проверяем Python..."
                    python --version
                    if ($LASTEXITCODE -ne 0) {
                        Write-Host "Python не найден, проверьте PATH" -ForegroundColor Red
                        exit 1
                    }
                    
                    Write-Host "Обновляем pip..."
                    python -m pip install --upgrade pip
                    
                    Write-Host "Устанавливаем зависимости..."
                    pip install selenium webdriver-manager pytest pytest-html allure-pytest pytest-xdist python-dotenv
                    
                    Write-Host "Список установленных пакетов:"
                    pip list | Select-String -Pattern "selenium|pytest|allure"
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                powershell '''
                    Write-Host "=== ЗАПУСК ТЕСТОВ ==="
                    
                    Write-Host "Создаем директории для отчетов..."
                    if (!(Test-Path "reports")) { New-Item -ItemType Directory -Path "reports" }
                    if (!(Test-Path "reports\\allure-results")) { New-Item -ItemType Directory -Path "reports\\allure-results" }
                    if (!(Test-Path "reports\\html")) { New-Item -ItemType Directory -Path "reports\\html" }
                    
                    Write-Host "Запускаем тесты..."
                    $testCommand = @"
python -m pytest tests/ `
    --junitxml=reports\\junit.xml `
    --html=reports\\html\\report.html `
    --self-contained-html `
    -n $env:PARALLEL_WORKERS `
    --timeout=300 `
    -v
"@
                    
                    Invoke-Expression $testCommand
                    
                    Write-Host "Код завершения тестов: $LASTEXITCODE"
                '''
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports\\**\\*', fingerprint: true
            
            publishHTML(target: [
                reportDir: 'reports/html',
                reportFiles: 'report.html',
                reportName: 'HTML Test Report',
                keepAll: true
            ])
            
            powershell '''
                Write-Host "=== ОЧИСТКА ==="
                Write-Host "Удаляем временные файлы..."
                if (Test-Path ".env") { Remove-Item ".env" }
                Write-Host "Готово!"
            '''
        }
    }
}