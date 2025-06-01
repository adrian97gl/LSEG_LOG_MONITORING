pipeline {
    agent any

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }
        stage('Clone repository') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'github_pat_adrian', usernameVariable: 'GITHUB_USER', passwordVariable: 'GITHUB_TOKEN')]) {
                            sh '''
                                git clone https://github.com/adrian97gl/LSEG_LOG_MONITORING.git
                                cd LSEG_LOG_MONITORING
                            '''
                }
            }
        }

        stage('Login && Build docker image') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'dockerhub-adrian', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        cd LSEG_LOG_MONITORING
                        echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
                        docker build -t $DOCKER_USERNAME/lseg-log-monitor-jenkins:latest .
                    '''
                }
            }
        }

        stage('Run Tests in Container') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-adrian', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh '''
                        docker run --name test-container $DOCKER_USERNAME/lseg-log-monitor-jenkins:latest /bin/bash -c "mkdir -p /tmp/test-results && pytest --cov=app --cov-report=html:/tmp/test-results/html tests/"
                        docker cp test-container:/tmp/test-results ./test-results
                        docker rm test-container
                    '''
                }
            }
        }

        stage('Archive Test Results') {
            steps {
                archiveArtifacts artifacts: 'test-results/**/*', allowEmptyArchive: true
            }
        }

        stage('Publish HTML Report') {
            steps {
                publishHTML(target: [
                    reportDir: 'test-results/html',
                    reportFiles: 'index.html',
                    reportName: 'Code Coverage Report'
                ])
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-adrian', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                    sh 'docker push $DOCKER_USERNAME/lseg-log-monitor-jenkins'
                }
            }
        }


    }
}