pipeline {
    agent any
    
    parameters {
        string(
            name: 'SELENOID_URL',
            defaultValue: 'http://selenoid:4444/wd/hub',
            description: 'Selenoid hub URL'
        )
        
        string(
            name: 'APP_URL',
            defaultValue: 'https://www.saucedemo.com',
            description: 'Application under test URL'
        )
        
        choice(
            name: 'BROWSER',
            choices: ['chrome', 'firefox', 'edge'],
            description: 'Browser for tests'
        )
        
        string(
            name: 'BROWSER_VERSION',
            defaultValue: 'latest',
            description: 'Browser version'
        )
        
        choice(
            name: 'THREADS',
            choices: ['1', '2', '3', '4', 'auto'],
            description: 'Number of parallel threads'
        )
        
        string(
            name: 'BRANCH',
            defaultValue: 'main',
            description: 'Git branch to build'
        )
        
        choice(
            name: 'TEST_SUITE',
            choices: ['all', 'smoke', 'regression', 'login', 'cart', 'purchase'],
            description: 'Test suite to execute'
        )
        
        choice(
            name: 'ENVIRONMENT',
            choices: ['development', 'staging', 'production'],
            description: 'Target environment'
        )
    }
    
    environment {
        PYTHONPATH = "${WORKSPACE}"
        BASE_URL = "${params.APP_URL}"
        USE_SELENOID = "${params.SELENOID_URL ? 'true' : 'false'}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${params.BRANCH}"]],
                    userRemoteConfigs: [[
                        url: https://github.com/Vladimir180791/pwa-hw37.git,
                        credentialsId: 'github-credentials'
                    ]]
                ])
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                echo "=== Build Parameters ==="
                echo "SELENOID_URL: ${SELENOID_URL}"
                echo "APP_URL: ${APP_URL}"
                echo "BROWSER: ${BROWSER}"
                echo "BROWSER_VERSION: ${BROWSER_VERSION}"
                echo "THREADS: ${THREADS}"
                echo "BRANCH: ${BRANCH}"
                echo "TEST_SUITE: ${TEST_SUITE}"
                echo "ENVIRONMENT: ${ENVIRONMENT}"
                echo "========================="
                
                # Create .env file with parameters
                cat > .env << EOF
                BASE_URL=${APP_URL}
                BROWSER=${BROWSER}
                ENVIRONMENT=${ENVIRONMENT}
                USE_SELENOID=${USE_SELENOID}
                SELENOID_HUB=${SELENOID_URL}
                BROWSER_VERSION=${BROWSER_VERSION}
                EOF
                
                # Install dependencies
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    def pytestCmd = "pytest -v"
                    
                    // Add test suite selection
                    switch(params.TEST_SUITE) {
                        case 'smoke':
                            pytestCmd += " -m smoke"
                            break
                        case 'regression':
                            pytestCmd += " -m regression"
                            break
                        case 'login':
                            pytestCmd += " tests/test_login.py"
                            break
                        case 'cart':
                            pytestCmd += " tests/test_cart.py"
                            break
                        case 'purchase':
                            pytestCmd += " tests/test_purchase.py"
                            break
                        default: // 'all'
                            pytestCmd += " tests/"
                    }
                    
                    // Add parallel execution
                    if (params.THREADS != "1") {
                        pytestCmd += " -n ${params.THREADS}"
                    }
                    
                    // Add allure reporting
                    pytestCmd += " --alluredir=reports/allure-results"
                    
                    // Add custom parameters
                    pytestCmd += " --browser=${params.BROWSER}"
                    pytestCmd += " --env=${params.ENVIRONMENT}"
                    
                    echo "Executing command: ${pytestCmd}"
                    sh pytestCmd
                }
            }
        }
        
        stage('Generate Reports') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    results: [[path: 'reports/allure-results']]
                ])
                
                // Archive artifacts
                archiveArtifacts artifacts: 'reports/**/*, screenshots/**/*, logs/**/*', fingerprint: true
            }
        }
    }
    
    post {
        always {
            echo "Build ${currentBuild.currentResult} - ${env.JOB_NAME} #${env.BUILD_NUMBER}"
            cleanWs()
        }
        success {
            echo '✅ All tests passed successfully!'
        }
        failure {
            echo '❌ Some tests failed! Check the reports.'
        }
    }
}