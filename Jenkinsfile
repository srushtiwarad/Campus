pipeline {
    agent any

    stages {
        stage('Clone Repo') {
             {
                git 'https://github.com/srushtiwarad/Campus.git'
            }
        }

        stage('Build Docker Image') {
             {
                sh 'docker build -t campus-complaint .'
            }
        }

        stage('Run Container') {
             {
                sh 'docker run -d -p 5000:5000 campus-complaint'
            }
        }
    }
}
