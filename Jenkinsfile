pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Login && Build docker image') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'dockerhub_adrian', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker build -t $DOCKER_USERNAME/lseg-log-monitor-jenkins:latest .
                    '''
                }
            }
        }

        stage('Run Tests in Container') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_adrian', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        docker run --name test-container $DOCKER_USERNAME/lseg-log-monitor-jenkins:latest pytest tests/
                        docker rm test-container
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub_adrian', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker push $DOCKER_USERNAME/lseg-log-monitor-jenkins'
                }
            }
        }
    }
}