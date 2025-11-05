pipeline {
    agent any

    environment {
        // Имена файлов отчётов
        QEMU_LOG         = 'qemu.log'
        API_TEST_REPORT  = 'api-test-results.xml'
        WEBUI_TEST_REPORT = 'webui-test-results.xml'
        LOAD_TEST_REPORT = 'load-test-results.json'
        
        // Путь к PID QEMU для корректного завершения
        QEMU_PID_FILE    = '/tmp/qemu.pid'
    }

    options {
        timeout(time: 15, unit: 'MINUTES')  // Защита от зависаний
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir pytest requests selenium locust
                '''
            }
        }

        stage('Start OpenBMC in QEMU') {
            steps {
                script {
                    sh '''
                        echo "🔧 Запуск OpenBMC в QEMU..."
                        ./scripts/run-openbmc.sh
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: "${QEMU_LOG}", allowEmptyArchive: true
                }
            }
        }

        stage('Run API (Redfish) Tests') {
            steps {
                sh '''
                    echo "🧪 Запуск API-тестов..."
                    . venv/bin/activate
                    cd tests
                    python3 -m pytest test_bmc_api.py --junitxml="../${API_TEST_REPORT}" -v
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: "${API_TEST_REPORT}", allowEmptyArchive: true
                    junit testResults: "${API_TEST_REPORT}", skipPublishingChecks: true
                }
            }
        }

        stage('Run WebUI Tests') {
            steps {
                sh '''
                    echo "🌐 Запуск WebUI-тестов..."
                    . venv/bin/activate
                    cd webui-tests
                    xvfb-run -a python3 -m pytest test_webui.py --junitxml="../${WEBUI_TEST_REPORT}" -v
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: "${WEBUI_TEST_REPORT}", allowEmptyArchive: true
                    junit testResults: "${WEBUI_TEST_REPORT}", skipPublishingChecks: true
                }
            }
        }

        stage('Run Load Tests') {
            steps {
                sh '''
                    echo "⚡ Запуск нагрузочного тестирования..."
                    . venv/bin/activate
                    cd load-tests
                    locust -f locustfile.py --headless \
                        --users 5 \
                        --spawn-rate 1 \
                        --run-time 60s \
                        --only-summary \
                        --json > "../${LOAD_TEST_REPORT}"
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: "${LOAD_TEST_REPORT}", allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            script {
                echo "⏹️  Остановка QEMU (если запущен)..."
                sh '''
                    if [ -f "${QEMU_PID_FILE}" ]; then
                        PID=$(cat "${QEMU_PID_FILE}")
                        if kill -0 $PID 2>/dev/null; then
                            echo "Убиваем процесс QEMU с PID=$PID"
                            kill $PID
                            wait $PID 2>/dev/null || true
                        else
                            echo "Процесс QEMU уже завершён"
                        fi
                        rm -f "${QEMU_PID_FILE}"
                    else
                        echo "Файл PID не найден — QEMU, возможно, не запускался"
                    fi
                '''
            }
        }
        success {
            echo "✅ Пайплайн завершён успешно!"
        }
        failure {
            echo "❌ Пайплайн завершился с ошибкой"
        }
    }
}