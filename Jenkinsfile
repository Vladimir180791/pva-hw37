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
        ENV_NAME = "${params.ENVIRONMENT}"
        BRWS = "${params.BROWSER}"
        HDLESS = "${params.HEADLESS}"
        B_URL = "${params.BASE_URL}"
        P_WORKERS = "${params.PARALLEL_WORKERS}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                
                bat """
                    echo CHECKING FILES
                    dir /b
                """
            }
        }
        
        stage('Check and Install Python') {
            steps {
                bat """
                    echo === CHECKING PYTHON INSTALLATION ===
                    
                    rem Проверяем, установлен ли Python
                    where python 2>nul
                    if %ERRORLEVEL% EQU 0 (
                        echo Python уже установлен
                        python --version
                    ) else (
                        echo Python не найден, проверяем другие варианты...
                        
                        rem Проверяем python3
                        where python3 2>nul
                        if %ERRORLEVEL% EQU 0 (
                            echo Найден python3
                            python3 --version
                            rem Создаем симлинк python -> python3
                            mklink python.exe python3.exe 2>nul || echo Не удалось создать симлинк
                        ) else (
                            echo ERROR: Python не установлен на этом агенте
                            echo Установите Python и добавьте в PATH
                            echo ИЛИ используйте агент с предустановленным Python
                            exit 1
                        )
                    )
                """
            }
        }
        
        stage('Setup Environment') {
            steps {
                bat """
                    echo === SETUP ENVIRONMENT ===
                    echo Environment: %ENV_NAME%
                    echo Browser: %BRWS%
                    echo Headless: %HDLESS%
                    echo Base URL: %B_URL%
                    
                    rem Create simple .env file
                    echo BASE_URL=%B_URL% > test_config.txt
                    echo BROWSER=%BRWS% >> test_config.txt
                    echo HEADLESS=%HDLESS% >> test_config.txt
                    echo STANDARD_USER=standard_user >> test_config.txt
                    echo STANDARD_PASSWORD=secret_sauce >> test_config.txt
                    
                    type test_config.txt
                """
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat """
                    echo === INSTALL DEPENDENCIES ===
                    
                    echo Final Python check:
                    python --version || python3 --version || (
                        echo CRITICAL: Python все еще не найден
                        echo Установите Python на Jenkins агенте
                        exit 1
                    )
                    
                    echo Updating pip...
                    python -m pip install --upgrade pip || python3 -m pip install --upgrade pip
                    
                    echo Installing dependencies from requirements.txt...
                    if exist requirements.txt (
                        echo Found requirements.txt
                        pip install -r requirements.txt || python3 -m pip install -r requirements.txt
                    ) else (
                        echo Installing minimal dependencies...
                        pip install selenium webdriver-manager pytest pytest-html || python3 -m pip install selenium webdriver-manager pytest pytest-html
                    )
                    
                    echo Installed packages:
                    pip list || python3 -m pip list
                """
            }
        }
        
        stage('Run Simple Test') {
            steps {
                bat """
                    echo === RUNNING SIMPLE TEST ===
                    
                    echo Creating simple test to verify installation...
                    echo import pytest > simple_test.py
                    echo def test_simple(): >> simple_test.py
                    echo     assert 1 == 1 >> simple_test.py
                    
                    echo Running test...
                    python -m pytest simple_test.py -v || python3 -m pytest simple_test.py -v
                    
                    del simple_test.py 2>nul
                """
            }
        }
        
        stage('Run Real Tests') {
            when {
                expression { return true }
            }
            steps {
                bat """
                    echo === RUNNING REAL TESTS ===
                    
                    echo Creating report directories...
                    if not exist reports mkdir reports
                    if not exist reports\\html mkdir reports\\html
                    
                    echo Running tests with %P_WORKERS% workers...
                    python -m pytest tests/ ^
                        --junitxml=reports\\junit.xml ^
                        --html=reports\\html\\report.html ^
                        --self-contained-html ^
                        -n %P_WORKERS% ^
                        --timeout=300 ^
                        -v
                    
                    echo Exit code: %ERRORLEVEL%
                """
            }
        }
    }
    
    post {
        always {
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
                    echo "Error archiving reports: ${e}"
                }
            }
            
            bat """
                echo === CLEANUP ===
                del test_config.txt 2>nul
                echo Done
            """
        }
        
        success {
            echo "TESTS PASSED SUCCESSFULLY"
        }
        
        failure {
            echo "TESTS FAILED"
        }
    }
}