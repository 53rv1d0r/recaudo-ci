pipeline {
    agent any

    environment {
        COMPOSE_PROJECT = "recaudo_ci_${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh "docker-compose -p ${COMPOSE_PROJECT} build"
            }
        }

        stage('Test') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'recaudo-db-credentials',
                    usernameVariable: 'DB_USER',
                    passwordVariable: 'DB_PASSWORD'
                )]) {
                    sh '''
                        set -e
                        POSTGRES_USER="$DB_USER" POSTGRES_PASSWORD="$DB_PASSWORD" POSTGRES_DB="recaudo_test" \
                            docker-compose -p "$COMPOSE_PROJECT" up -d --wait
                        docker-compose -p "$COMPOSE_PROJECT" exec -T api pytest -v
                    '''
                }
            }
        }
    }

    post {
        always {
            sh "docker-compose -p ${COMPOSE_PROJECT} down -v --remove-orphans || true"
        }
        success {
            echo "Build ${env.BUILD_NUMBER} exitoso: pruebas y conexion con db aprobadas."
        }
        failure {
            echo "Build ${env.BUILD_NUMBER} fallido: revisa la etapa en rojo."
        }
    }
}