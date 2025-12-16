pipeline {
    agent any
    
    parameters {
        choice(name: 'ENVIRONMENT', choices: ['development', 'staging', 'production'], description: 'Test environment')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Browser for tests')
        choice(name: 'HEADLESS', choices: ['true', 'false'], description: 'Run in headless mode')
        string(name: 'BASE_URL', defaultValue: 'https://www.saucedemo.com', description: 'Application URL')
        string(name: 'PARALLEL_WORKERS', defaultValue: '2', description: 'Number of parallel workers')
    }
    
    // Используем английские имена переменных без кириллицы
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
                
                // Проверка что файлы загрузились
                bat """
                    echo CHECKING FILES
                    dir /b
                """
            }
        }
        
        stage('Setup Environment') {
            steps {
                // Используем простой bat с ASCII символами
                bat """
                    echo === SETUP ENVIRONMENT ===
                    echo Environment: %ENV_NAME%
                    echo Browser: %BRWS%
                    echo Headless: %HDLESS%
                    echo Base URL: %B_URL%
                    
                    rem Create simple .env file without complex characters
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
                    
                    echo Checking Python...
                    python --version
                    if errorlevel 1 (
                        echo ERROR: Python not found
                        exit 1
                    )
                    
                    echo Updating pip...
                    python -m pip install --upgrade pip
                    
                    echo Installing dependencies...
                    pip install selenium webdriver-manager pytest pytest-html
                    
                    echo Installed packages:
                    pip list | findstr /i "selenium pytest"
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
            // Archive reports if they exist
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
            
            // Cleanup
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