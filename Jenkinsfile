pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/srushtiwarad/Campus.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t campus-image .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d --name campus-container campus-image'
            }
        }
    }
}
