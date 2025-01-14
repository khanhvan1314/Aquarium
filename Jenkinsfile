pipeline {
    agent any

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

                # Kích hoạt Anaconda và cài đặt dependencies
                source /opt/anaconda3/bin/activate
                pip install --upgrade pip setuptools
                pip install -r requirements.txt
                '''
            }
        }

        // Stage 3: Run Tests
        stage('Run Tests') {
            steps {
                sh '''
                # Sử dụng đường dẫn đầy đủ tới pytest
                /opt/anaconda3/bin/pytest test_api.py || exit 1
                '''
            }
        }

        // Stage 4: Deploy API
        stage('Deploy API') {
            steps {
                sh '''
                # Tìm và dừng tiến trình trên cổng 8000 (nếu có)
                if lsof -ti:8000; then
                    echo "Killing process on port 8000..."
                    lsof -ti:8000 | xargs kill -9
                else
                    echo "No process found on port 8000."
                fi

                # Khởi chạy API bằng Uvicorn và ghi logs
                echo "Starting API on port 8000..."
                nohup uvicorn deploy:app --host 0.0.0.0 --port 8000 > uvicorn.log 2>&1 &

                # Chờ 5 giây để API khởi động
                sleep 5

                # Kiểm tra xem API có đang chạy hay không
                if lsof -ti:8000; then
                    echo "API is running successfully on port 8000."
                else
                    echo "Failed to start API on port 8000. Check logs:"
                    cat uvicorn.log
                    exit 1
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
        always {
            echo 'Pipeline finished.'
        }
    }
}
