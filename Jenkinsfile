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
        // Указываем конкретный путь к Python, если он установлен
        PYTHON_PATH = "C:\\Python311\\python.exe"  // Измените путь, если Python установлен в другом месте
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                
                bat """
                    echo === CHECKING FILES IN WORKSPACE ===
                    dir /b
                    echo.
                    echo === CHECKING PYTHON INSTALLATIONS ===
                    where python 2>nul || echo Python not found in PATH
                    where python3 2>nul || echo Python3 not found in PATH
                """
            }
        }
        
        stage('Check and Install Python') {
            steps {
                script {
                    // Проверяем установлен ли Python
                    def pythonInstalled = bat(
                        script: 'where python 2>nul',
                        returnStatus: true
                    ) == 0
                    
                    if (!pythonInstalled) {
                        echo "Python not found in PATH. Trying to find in common locations..."
                        
                        // Проверяем стандартные места установки Python
                        def pythonPaths = [
                            'C:\\Python311\\python.exe',
                            'C:\\Python310\\python.exe',
                            'C:\\Python39\\python.exe',
                            'C:\\Python38\\python.exe',
                            'C:\\Python\\python.exe',
                            'C:\\Program Files\\Python311\\python.exe',
                            'C:\\Program Files\\Python310\\python.exe',
                            'C:\\Program Files\\Python39\\python.exe',
                            'C:\\Program Files\\Python38\\python.exe',
                            'C:\\Program Files\\Python\\python.exe'
                        ]
                        
                        def foundPython = false
                        for (path in pythonPaths) {
                            def exists = bat(
                                script: "if exist \"${path}\" echo FOUND",
                                returnStatus: true
                            ) == 0
                            
                            if (exists) {
                                env.PYTHON_EXE = path
                                foundPython = true
                                echo "Found Python at: ${path}"
                                break
                            }
                        }
                        
                        if (!foundPython) {
                            echo "Python not found. Attempting to install..."
                            // Добавляем опциональную установку Python через chocolatey
                            bat '''
                                echo === ATTEMPTING TO INSTALL PYTHON ===
                                echo Please ensure Python 3.11+ is installed on the system
                                echo.
                                echo To install Python:
                                echo 1. Download from https://www.python.org/downloads/
                                echo 2. Run installer with "Add Python to PATH" checked
                                echo 3. Or install using chocolatey: choco install python --version=3.11.9
                                echo.
                                exit 1
                            '''
                        }
                    } else {
                        env.PYTHON_EXE = "python"
                    }
                }
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
                    
                    rem Проверяем Python
                    echo Checking Python executable...
                    "%PYTHON_EXE%" --version || echo Python not accessible
                    
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
                    
                    echo Checking Python executable: %PYTHON_EXE%
                    "%PYTHON_EXE%" --version
                    if errorlevel 1 (
                        echo ERROR: Python not found or not accessible
                        echo Trying alternative methods...
                        
                        rem Попробуем найти python через py launcher
                        py --version
                        if errorlevel 1 (
                            echo ERROR: No Python installation found
                            echo Please install Python 3.11 or higher
                            exit 1
                        ) else (
                            set PYTHON_EXE=py
                        )
                    )
                    
                    echo Using Python: %PYTHON_EXE%
                    
                    echo Updating pip...
                    "%PYTHON_EXE%" -m pip install --upgrade pip
                    
                    echo Installing dependencies with specific versions for compatibility...
                    rem Устанавливаем конкретные версии для совместимости
                    "%PYTHON_EXE%" -m pip install selenium==4.15.0
                    "%PYTHON_EXE%" -m pip install webdriver-manager==4.0.1
                    "%PYTHON_EXE%" -m pip install pytest==7.4.4
                    "%PYTHON_EXE%" -m pip install pytest-html==4.1.1
                    "%PYTHON_EXE%" -m pip install pytest-xdist==3.5.0
                    "%PYTHON_EXE%" -m pip install pytest-timeout==2.2.0
                    
                    echo Installed packages:
                    "%PYTHON_EXE%" -m pip list | findstr /i "selenium pytest webdriver"
                """
            }
        }
        
        stage('Verify Installation') {
            steps {
                bat """
                    echo === VERIFYING INSTALLATION ===
                    
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
                    "%PYTHON_EXE%" -m pytest simple_test.py -v
                    
                    del simple_test.py 2>nul
                """
            }
        }
        
        stage('Run Tests') {
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
                    "%PYTHON_EXE%" -m pytest tests/ ^
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
                        where python 2>nul
                        echo Python executable used: %PYTHON_EXE%
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
                where python 2>nul || echo Python not found
                where python3 2>nul || echo Python3 not found
                where py 2>nul || echo py launcher not found
            """
        }
    }
}