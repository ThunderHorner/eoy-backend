pipeline {
    agent any

    environment {
        // Repository and server configuration
        GIT_REPO_URL = 'git@github.com:ThunderHorner/eoy-backend.git'
        DOCKER_SERVER = 'thunderhorn@192.168.0.103'
        REMOTE_DIR = '/home/thunderhorn/crypto_tip_backend'
        APP_PORT = 8000 // Update to match your application port
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the specified branch from the GitHub repository
                git branch: 'main', credentialsId: '10', url: "${env.GIT_REPO_URL}"
            }
        }

        stage('SSH to Server and Deploy') {
            steps {
                script {
                    sshagent(['15']) {
                        sh """
                        # Connect to the server and prepare the deployment directory
                        ssh -o StrictHostKeyChecking=no ${DOCKER_SERVER} '
                            rm -rf ${REMOTE_DIR} &&
                            mkdir -p ${REMOTE_DIR}'

                        # Copy project files to the remote server
                        scp -r ./* ${DOCKER_SERVER}:${REMOTE_DIR}/

                        # Execute deployment steps on the server
                        ssh -o StrictHostKeyChecking=no ${DOCKER_SERVER} '
                            cd ${REMOTE_DIR} &&
                            ./build.sh &&
                            sleep 5 &&
                            docker ps | grep crypto_tip_backend || echo "Container failed to start!"'
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up workspace after the build
            cleanWs()
        }
    }
}
