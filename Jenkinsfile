pipeline {
    agent any

    stages {
        // Stage 1: Clone Repository
        stage('Clone Repository') {
            steps {
                git 'https://github.com/khanhvan1314/Aquarium.git'  // Thay bằng URL repository của bạn
            }
        }

        // Stage 2: Install Dependencies
        stage('Install Dependencies') {
            steps {
                sh '''
                # Cài đặt thư viện trực tiếp
                pip install --upgrade pip setuptools
                pip install -r requirements.txt
                '''
            }
        }

        // Stage 3: Run Tests
        stage('Run Tests') {
            steps {
                sh '''
                pytest test_api.py                      # Chạy kiểm thử
                '''
            }
        }

        // Stage 4: Deploy API
        stage('Deploy API') {
            steps {
                sh '''
                # Tìm và dừng tiến trình trên cổng 8000 (nếu có)
                lsof -ti:8000 | xargs kill -9 || true

                # Khởi động API
                nohup uvicorn deploy:app --host 0.0.0.0 --port 8000 &

                # Chờ để đảm bảo API khởi chạy
                sleep 5

                # Kiểm tra API có chạy không
                if ! lsof -i :8000; then
                    echo "API failed to start"
                    exit 1
                else
                    echo "API is running on port 8000"
                fi
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
