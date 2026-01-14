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
        // Указываем путь к Python (из логов видно, что Python есть в C:\Program Files\Python311\python.exe)
        PYTHON_EXE = "python"  // Используем просто python, так как он в PATH
    }
    
    stages {
        stage('Checkout and Setup') {
            steps {
                checkout scm
                
                bat """
                    echo === CHECKING FILES IN WORKSPACE ===
                    dir /b
                    echo.
                    echo === CHECKING PYTHON INSTALLATIONS ===
                    where python
                    python --version
                    
                    echo === SETTING PYTHON PATH ===
                    rem Проверяем доступность Python
                    python --version
                    if errorlevel 1 (
                        echo ERROR: Python not accessible via 'python' command
                        echo Trying direct path...
                        "C:\\Program Files\\Python311\\python.exe" --version
                        if errorlevel 1 (
                            echo ERROR: Python not found
                            exit 1
                        ) else (
                            echo Found Python at C:\\Program Files\\Python311\\python.exe
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
                    echo Parallel Workers: %P_WORKERS%
                    
                    rem Сначала определим правильный путь к Python
                    python --version
                    if errorlevel 1 (
                        set PYTHON_EXE="C:\\Program Files\\Python311\\python.exe"
                    ) else (
                        set PYTHON_EXE=python
                    )
                    
                    echo Using Python executable: %PYTHON_EXE%
                    
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
                    
                    rem Определяем Python executable
                    python --version
                    if errorlevel 1 (
                        set PYTHON_EXE="C:\\Program Files\\Python311\\python.exe"
                    ) else (
                        set PYTHON_EXE=python
                    )
                    
                    echo Using Python: %PYTHON_EXE%
                    
                    echo Updating pip...
                    %PYTHON_EXE% -m pip install --upgrade pip
                    
                    echo Installing dependencies with specific versions for compatibility...
                    rem Устанавливаем конкретные версии для совместимости
                    %PYTHON_EXE% -m pip install selenium==4.15.0
                    %PYTHON_EXE% -m pip install webdriver-manager==4.0.1
                    %PYTHON_EXE% -m pip install pytest==7.4.4
                    %PYTHON_EXE% -m pip install pytest-html==4.1.1
                    %PYTHON_EXE% -m pip install pytest-xdist==3.5.0
                    %PYTHON_EXE% -m pip install pytest-timeout==2.2.0
                    
                    echo Installed packages:
                    %PYTHON_EXE% -m pip list | findstr /i "selenium pytest webdriver"
                """
            }
        }
        
        stage('Verify Installation') {
            steps {
                bat """
                    echo === VERIFYING INSTALLATION ===
                    
                    rem Определяем Python executable
                    python --version
                    if errorlevel 1 (
                        set PYTHON_EXE="C:\\Program Files\\Python311\\python.exe"
                    ) else (
                        set PYTHON_EXE=python
                    )
                    
                    echo Creating simple test to verify installation...
                    echo import pytest > simple_test.py
                    echo import selenium.webdriver >> simple_test.py
                    echo import sys >> simple_test.py
                    echo def test_python_version(): >> simple_test.py
                    echo     print(f"Python version: {sys.version}") >> simple_test.py
                    echo     assert sys.version_info[0] == 3, "Python 3 required" >> simple_test.py
                    echo def test_imports(): >> simple_test.py
                    echo     import selenium >> simple_test.py
                    echo     import pytest >> simple_test.py
                    echo     import webdriver_manager >> simple_test.py
                    echo     assert True >> simple_test.py
                    
                    echo Running verification test...
                    %PYTHON_EXE% -m pytest simple_test.py -v
                    
                    del simple_test.py 2>nul
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                bat """
                    echo === RUNNING REAL TESTS ===
                    
                    rem Определяем Python executable
                    python --version
                    if errorlevel 1 (
                        set PYTHON_EXE="C:\\Program Files\\Python311\\python.exe"
                    ) else (
                        set PYTHON_EXE=python
                    )
                    
                    echo Creating report directories...
                    if not exist reports mkdir reports
                    if not exist reports\\html mkdir reports\\html
                    if not exist reports\\xml mkdir reports\\xml
                    
                    echo Running tests with %P_WORKERS% workers...
                    %PYTHON_EXE% -m pytest tests/ ^
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
                        echo Python path:
                        where python
                        echo Python executable used: %PYTHON_EXE%
                        echo === TESTS CONTENT ===
                        if exist tests\\*.py (
                            type tests\\*.py
                        )
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
            // Добавляем дополнительную информацию для диагностики
            bat """
                echo === DIAGNOSTIC INFORMATION ===
                echo System PATH:
                echo %PATH%
                echo.
                echo Python installations:
                where python
                echo.
                echo Files in tests directory:
                if exist tests\\ (
                    dir tests\\ /b
                )
            """
        }
    }
}