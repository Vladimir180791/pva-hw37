pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['development', 'staging', 'production'], description: 'Test environment')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser for tests')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        string(name: 'BASE_URL', defaultValue: 'https://www.saucedemo.com', description: 'Application URL')
        string(name: 'TIMEOUT', defaultValue: '30', description: 'Timeout for page load (seconds)')
    }
    
    environment {
        ENV_NAME = "${params.ENVIRONMENT}"
        BRWS = "${params.BROWSER}"
        HDLESS = "${params.HEADLESS}"
        B_URL = "${params.BASE_URL}"
        TIMEOUT_VAL = "${params.TIMEOUT}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                
                bat """
                    echo === WORKSPACE FILES ===
                    dir /b
                    echo.
                    echo === PYTHON INFO ===
                    python --version
                    python -c "import sys; print(f'Platform: {sys.platform}')"
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
                    echo Timeout: %TIMEOUT_VAL%
                    
                    rem Создаем .env файл
                    echo BASE_URL=%B_URL% > .env
                    echo BROWSER=%BRWS% >> .env
                    echo HEADLESS=%HDLESS% >> .env
                    echo ENVIRONMENT=%ENV_NAME% >> .env
                    echo STANDARD_USER=standard_user >> .env
                    echo STANDARD_PASSWORD=secret_sauce >> .env
                    echo TIMEOUT=%TIMEOUT_VAL% >> .env
                    
                    echo === .env content ===
                    type .env
                    
                    echo === CHROME CHECK ===
                    where chrome 2>nul && (
                        echo ✓ Chrome found in PATH
                        chrome --version
                    ) || (
                        echo ⚠️ Chrome not found in PATH
                        echo Checking registry...
                        reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version 2>nul && (
                            for /f "tokens=2*" %%a in ('reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version 2^>nul') do echo Chrome version: %%b
                        ) || echo Chrome not installed
                    )
                """
            }
        }
        
        stage('Install Dependencies') {
            steps {
                bat """
                    echo === INSTALL DEPENDENCIES ===
                    
                    echo Updating pip...
                    python -m pip install --upgrade pip
                    
                    echo Installing dependencies...
                    python -m pip install selenium==4.15.0
                    python -m pip install webdriver-manager==4.0.1
                    python -m pip install pytest==7.4.4
                    python -m pip install pytest-html==4.1.1
                    python -m pip install pytest-xdist==3.5.0
                    python -m pip install python-dotenv==1.0.0
                    
                    echo === Installed packages ===
                    python -m pip list | findstr /i "selenium pytest webdriver"
                """
            }
        }
        
        stage('Clean WebDriver Cache') {
            steps {
                bat """
                    echo === CLEANING WEBDRIVER CACHE ===
                    
                    echo Cleaning up WebDriver Manager cache...
                    python -c "
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    ChromeDriverManager().clear_cache()
    GeckoDriverManager().clear_cache()
    print('✓ WebDriver cache cleaned')
except Exception as e:
    print(f'⚠️ Cache cleanup failed: {e}')
"
                    
                    echo Checking cache directory...
                    dir "%USERPROFILE%\\.wdm" /s 2>nul | findstr /i chromedriver && echo ✓ WebDriver cache exists || echo ⚠️ WebDriver cache not found
                """
            }
        }
        
        stage('Run Tests') {
            steps {
                bat """
                    echo === RUNNING TESTS ===
                    
                    echo Creating report directories...
                    if not exist reports mkdir reports
                    if not exist reports\\html mkdir reports\\html
                    if not exist reports\\xml mkdir reports\\xml
                    if not exist screenshots mkdir screenshots
                    
                    echo Running tests...
                    
                    rem Устанавливаем переменные окружения для тестов
                    set BASE_URL=%B_URL%
                    set BROWSER=%BRWS%
                    set HEADLESS=%HDLESS%
                    set TIMEOUT=%TIMEOUT_VAL%
                    
                    python -m pytest tests/ ^
                        --junitxml=reports\\xml\\junit.xml ^
                        --html=reports\\html\\report.html ^
                        --self-contained-html ^
                        -v ^
                        --tb=short
                    
                    echo Exit code: %ERRORLEVEL%
                    
                    if %ERRORLEVEL% NEQ 0 (
                        echo === DEBUG INFO ===
                        echo Python version:
                        python --version
                        echo.
                        echo Platform info:
                        python -c "import platform; print(f'System: {platform.system()} {platform.release()}')"
                        echo.
                        echo Files in tests directory:
                        dir tests\\ /b
                        echo.
                        echo Checking for screenshots...
                        if exist screenshots\\*.png (
                            echo Screenshots found:
                            dir screenshots\\ /b
                        ) else (
                            echo No screenshots found
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
                    // Архивируем отчеты и скриншоты
                    if (fileExists('reports/html/report.html')) {
                        archiveArtifacts artifacts: 'reports/**/*', fingerprint: true
                        
                        publishHTML(target: [
                            reportDir: 'reports/html',
                            reportFiles: 'report.html',
                            reportName: 'Test Report',
                            keepAll: true
                        ])
                    }
                    
                    if (fileExists('reports/xml/junit.xml')) {
                        junit 'reports/xml/junit.xml'
                    }
                    
                    // Архивируем скриншоты, если они есть
                    if (fileExists('screenshots')) {
                        def screenshots = findFiles(glob: 'screenshots/*.png')
                        if (screenshots) {
                            archiveArtifacts artifacts: 'screenshots/*.png', fingerprint: false
                        }
                    }
                } catch (Exception e) {
                    echo "Error archiving reports: ${e}"
                }
            }
            
            bat """
                echo === CLEANUP ===
                echo Cleaning up...
                del .env 2>nul
                echo Done
            """
        }
        
        success {
            echo "✓ TESTS PASSED SUCCESSFULLY"
            emailext (
                subject: "✅ Tests PASSED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "All tests passed successfully.\n\nBuild URL: ${env.BUILD_URL}",
                to: 'vladimir@example.com'
            )
        }
        
        failure {
            echo "✗ TESTS FAILED"
            
            // Дополнительная диагностика
            bat """
                echo === ADDITIONAL DIAGNOSTICS ===
                echo Chrome installation check:
                where chrome 2>nul || echo Chrome not found
                echo.
                echo WebDriver cache:
                dir "%USERPROFILE%\\.wdm\\drivers\\chromedriver" /s 2>nul | findstr /i .exe || echo No ChromeDriver found
                echo.
                echo Python packages:
                python -m pip list | findstr selenium
            """
            
            emailext (
                subject: "❌ Tests FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: "Tests failed. Please check the build logs.\n\nBuild URL: ${env.BUILD_URL}\n\nFailed tests may require investigation.",
                to: 'vladimir@example.com'
            )
        }
        
        unstable {
            echo "⚠️ TESTS ARE UNSTABLE"
        }
    }
}