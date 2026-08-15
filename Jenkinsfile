pipeline {

    agent any

    environment {
        DOCKERHUB_USER = 'malovikas'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from GitHub...'
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                echo 'Building FoodGo Docker images...'

                sh '''
                    docker build -t ${DOCKERHUB_USER}/foodgo-user-service:v1 ./backend/user-service

                    docker build -t ${DOCKERHUB_USER}/foodgo-restaurant-service:v1 ./backend/restaurant-service

                    docker build -t ${DOCKERHUB_USER}/foodgo-order-service:v1 ./backend/order-service

                    docker build -t ${DOCKERHUB_USER}/foodgo-payment-service:v1 ./backend/payment-service

                    docker build -t ${DOCKERHUB_USER}/foodgo-api-gateway:v1 ./backend/api-gateway

                    docker build -t ${DOCKERHUB_USER}/foodgo-frontend:v1 ./frontend
                '''
            }
        }

        stage('Docker Images') {
            steps {
                echo 'Displaying FoodGo Docker images...'

                sh '''
                    docker images | grep foodgo
                '''
            }
        }

        stage('Push Images to Docker Hub') {
            steps {
                echo 'Pushing FoodGo images to Docker Hub...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {

                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                            -u "$DOCKER_USERNAME" \
                            --password-stdin

                        docker push ${DOCKERHUB_USER}/foodgo-user-service:v1

                        docker push ${DOCKERHUB_USER}/foodgo-restaurant-service:v1

                        docker push ${DOCKERHUB_USER}/foodgo-order-service:v1

                        docker push ${DOCKERHUB_USER}/foodgo-payment-service:v1

                        docker push ${DOCKERHUB_USER}/foodgo-api-gateway:v1

                        docker push ${DOCKERHUB_USER}/foodgo-frontend:v1
                    '''
                }
            }
        }

        stage('Verify Images') {
            steps {
                echo 'Verifying Docker images...'

                sh '''
                    docker images | grep malovikas/foodgo
                '''
            }
        }
    }

    post {

        success {
            echo '======================================'
            echo 'JENKINS PIPELINE SUCCESSFUL'
            echo 'FoodGo images built and pushed!'
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