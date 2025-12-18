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
        
        stage('Check Python Version') {
            steps {
                bat """
                    echo === CHECKING PYTHON VERSION ===
                    python --version
                    
                    rem Проверяем что это не альфа/бета версия
                    python -c "import sys; print(f'Python {sys.version}'); exit(0) if sys.version_info[0:2] == (3, 11) else exit(1)"
                    if errorlevel 1 (
                        echo WARNING: Python version is not 3.11.x
                        echo Current version may have compatibility issues
                        echo Consider installing Python 3.11.9 for better compatibility
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
                    echo Parallel Workers: %P_WORKERS%
                    
                    rem Create .env file with all required variables
                    echo BASE_URL=%B_URL% > .env
                    echo BROWSER=%BRWS% >> .env
                    echo HEADLESS=%HDLESS% >> .env
                    echo ENVIRONMENT=%ENV_NAME% >> .env
                    echo STANDARD_USER=standard_user >> .env
                    echo STANDARD_PASSWORD=secret_sauce >> .env
                    echo TIMEOUT=10 >> .env
                    echo PARALLEL_WORKERS=%P_WORKERS% >> .env
                    
                    echo === .env file content ===
                    type .env
                """
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat """
                    echo === INSTALL DEPENDENCIES ===
                    
                    echo Checking Python...
                    python --version
                    if errorlevel 1 (
                        echo ERROR: Python not found
                        exit 1
                    )
                    
                    echo Updating pip...
                    python -m pip install --upgrade pip
                    
                    echo Installing dependencies with specific versions for compatibility...
                    rem Устанавливаем конкретные версии для совместимости
                    pip install selenium==4.15.0
                    pip install webdriver-manager==4.0.1
                    pip install pytest==7.4.4
                    pip install pytest-html==4.1.1
                    pip install pytest-xdist==3.5.0
                    pip install pytest-timeout==2.2.0
                    
                    echo Installed packages:
                    pip list | findstr /i "selenium pytest"
                """
            }
        }
        
        stage('Run Simple Test') {
            steps {
                bat """
                    echo === RUNNING SIMPLE TEST ===
                    
                    echo Creating simple test to verify installation...
                    echo import pytest > simple_test.py
                    echo import selenium >> simple_test.py
                    echo def test_import(): >> simple_test.py
                    echo     import selenium >> simple_test.py
                    echo     import pytest >> simple_test.py
                    echo     assert True >> simple_test.py
                    
                    echo Running test...
                    python -m pytest simple_test.py -v
                    
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
                    if not exist reports\\xml mkdir reports\\xml
                    
                    echo Running tests with %P_WORKERS% workers...
                    python -m pytest tests/ ^
                        --junitxml=reports\\xml\\junit.xml ^
                        --html=reports\\html\\report.html ^
                        --self-contained-html ^
                        -n %P_WORKERS% ^
                        --timeout=300 ^
                        -v
                    
                    echo Exit code: %ERRORLEVEL%
                    
                    rem Если тесты упали, покажем что в папке tests
                    if %ERRORLEVEL% NEQ 0 (
                        echo === TEST FAILURE DEBUG INFO ===
                        echo Checking tests directory...
                        dir tests\\ /b
                        echo Current directory:
                        dir /b
                    )
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
                    
                    // Archive JUnit reports
                    if (fileExists('reports/xml/junit.xml')) {
                        junit 'reports/xml/junit.xml'
                    }
                } catch (Exception e) {
                    echo "Error archiving reports: ${e}"
                }
            }
            
            bat """
                echo === CLEANUP ===
                del .env 2>nul
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