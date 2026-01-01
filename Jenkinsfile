pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
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
