pipeline {
    agent any

    environment {
        VENV_DIR = "./venv"  // Thư mục môi trường ảo Python
    }

    stages {
        // Stage 1: Clone Repository
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-repo/api-detection.git'  // Thay bằng URL repository của bạn
            }
        }

        // Stage 2: Install Dependencies
        stage('Install Dependencies') {
            steps {
                sh '''
                python -m venv ${VENV_DIR}                # Tạo môi trường ảo
                source ${VENV_DIR}/bin/activate          # Kích hoạt môi trường ảo
                pip install --upgrade pip setuptools    # Cập nhật pip
                pip install -r requirements.txt         # Cài đặt các thư viện
                '''
            }
        }

        // Stage 3: Run Tests
        stage('Run Tests') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate          # Kích hoạt môi trường ảo
                pytest test_api.py                      # Chạy kiểm thử
                '''
            }
        }

        // Stage 4: Deploy API
        stage('Deploy API') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate          # Kích hoạt môi trường ảo
                nohup uvicorn deploy:app --host 0.0.0.0 --port 8000 &  # Triển khai API
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
    }
}
