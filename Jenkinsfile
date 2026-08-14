pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building Docker images...'

                sh '''
                    docker build -t foodgo-frontend ./frontend

                    docker build -t foodgo-user-service \
                        -f backend/user-service/Dockerfile .

                    docker build -t foodgo-restaurant-service \
                        -f backend/restaurant-service/Dockerfile .

                    docker build -t foodgo-order-service \
                        -f backend/order-service/Dockerfile .

                    docker build -t foodgo-payment-service \
                        -f backend/payment-service/Dockerfile .
                '''
            }
        }

        stage('Docker Images') {
            steps {
                echo 'Displaying created Docker images...'

                sh '''
                    docker images | grep foodgo
                '''
            }
        }

        stage('Test Containers') {
            steps {
                echo 'Docker image build completed successfully.'
                echo 'Container testing will be added after Kubernetes setup.'
            }
        }
    }

    post {

        success {
            echo '======================================'
            echo 'JENKINS PIPELINE SUCCESSFUL'
            echo 'Docker images built successfully!'
            echo '======================================'
        }

        failure {
            echo '======================================'
            echo 'JENKINS PIPELINE FAILED'
            echo 'Check the console output for errors.'
            echo '======================================'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}