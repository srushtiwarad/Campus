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
                sh 'docker build -t campus-complaint .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5000:5000 campus-complaint'
            }
        }
    }
}
