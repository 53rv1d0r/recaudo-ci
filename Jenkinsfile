pipeline {
    agent any

    environment {
        NET_NAME = "recaudo_net_${env.BUILD_NUMBER}"
        DB_NAME  = "recaudo_db_${env.BUILD_NUMBER}"
        API_NAME = "recaudo_api_${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh """
                    set -e
                    docker build -f Dockerfile.db -t recaudo-ci-db:${env.BUILD_NUMBER} .
                    docker build -f Dockerfile -t recaudo-ci-api:${env.BUILD_NUMBER} .
                """
            }
        }

        stage('Test') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'recaudo-db-credentials',
                    usernameVariable: 'DB_USER',
                    passwordVariable: 'DB_PASSWORD'
                )]) {
                    sh """
                        set -e
                        docker network create ${NET_NAME}
                        docker run -d --name ${DB_NAME} --network ${NET_NAME} --network-alias db \
                            -e POSTGRES_DB=recaudo_test \
                            -e POSTGRES_USER="\$DB_USER" \
                            -e POSTGRES_PASSWORD="\$DB_PASSWORD" \
                            recaudo-ci-db:${env.BUILD_NUMBER}

                        sleep 4

                        docker run --rm --name ${API_NAME} --network ${NET_NAME} \
                            -e DB_HOST=db \
                            -e DB_PORT=5432 \
                            recaudo-ci-api:${env.BUILD_NUMBER} \
                            python -m pytest -v
                    """
                }
            }
        }
    }

    post {
        always {
            sh """
                docker rm -f ${API_NAME} ${DB_NAME} 2>/dev/null || true
                docker network rm ${NET_NAME} 2>/dev/null || true
                docker rmi -f recaudo-ci-db:${env.BUILD_NUMBER} recaudo-ci-api:${env.BUILD_NUMBER} 2>/dev/null || true
            """
        }
        success {
            echo "Build ${env.BUILD_NUMBER} exitoso: imagenes construidas y comunicacion con db verificada."
        }
        failure {
            echo "Build ${env.BUILD_NUMBER} fallido: revisa la etapa en rojo."
        }
    }
}