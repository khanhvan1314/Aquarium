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
                # Dừng API cũ nếu đang chạy
                if screen -list | grep -q "api_server"; then
                    screen -S api_server -X quit
                    echo "Stopped old API session."
                fi

                # Tạo session mới và chạy API
                echo "Starting API on port 8000 in screen session..."
                screen -dmS api_server /opt/anaconda3/bin/uvicorn deploy:app --host 0.0.0.0 --port 8001
                sleep 5

                # Kiểm tra API
                if lsof -ti:8001; then
                    echo "API is running successfully on port 8000."
                else
                    echo "Failed to start API on port 8000."
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
