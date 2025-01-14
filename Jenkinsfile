pipeline {
    agent any

    environment {
        VENV_DIR = "./venv"  // Thư mục môi trường ảo Python
    }

    stages {
        // Stage 1: Clone Repository
        stage('Clone Repository') {
            steps {
                git branch: 'main',  // Chỉ định nhánh main
                    credentialsId: 'github-aqua',  // ID credentials trong Jenkins
                    url: 'https://github.com/khanhvan1314/Aquarium.git'  // URL repo
            }
        }

        // Stage 2: Install Dependencies
        stage('Install Dependencies') {
            steps {
                sh '''
                if ! command -v python3 &> /dev/null; then
                    echo "Python3 is not installed. Please install Python3.";
                    exit 1;
                fi
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                pip install --upgrade pip setuptools
                pip install -r requirements.txt
                '''
            }
        }

        // Stage 3: Run Tests
        stage('Run Tests') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                pytest test_api.py || exit 1  # Dừng pipeline nếu pytest thất bại
                '''
            }
        }

        // Stage 4: Deploy API
        stage('Deploy API') {
            steps {
                sh '''
                if lsof -i:8000; then
                    echo "Port 8000 is already in use. Please free the port or use a different one.";
                    exit 1;
                fi
                source ${VENV_DIR}/bin/activate
                nohup uvicorn deploy:app --host 0.0.0.0 --port 8000 &
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            echo 'Pipeline finished.'
        }
    }
}
