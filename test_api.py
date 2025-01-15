import pytest
from fastapi.testclient import TestClient
from deploy import app  # Import ứng dụng từ file deploy.py

# Tạo TestClient để kiểm tra API
client = TestClient(app)

def test_root():
    """
    Kiểm tra endpoint gốc (/)
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Aquarium Detection API is running!"}

def test_predict_json():
    """
    Kiểm tra endpoint /predict/json với một ảnh hợp lệ
    """
    with open("test_image.jpg", "rb") as file:  # Đảm bảo có một ảnh test (test_image.jpg)
        response = client.post("/predict/json", files={"file": ("test_image.jpg", file, "image/jpeg")})
    assert response.status_code == 200
    assert "predictions" in response.json()
    assert isinstance(response.json()["predictions"], list)  # Đảm bảo predictions là danh sách

def test_predict_image():
    """
    Kiểm tra endpoint /predict/image với một ảnh hợp lệ
    """
    with open("test_image.jpg", "rb") as file:  # Đảm bảo có một ảnh test (test_image.jpg)
        response = client.post("/predict/image", files={"file": ("test_image.jpg", file, "image/jpeg")})
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"  # Đảm bảo phản hồi là ảnh

def test_invalid_file():
    """
    Kiểm tra khi gửi file không hợp lệ
    """
    response = client.post("/predict/json", files={"file": ("invalid.txt", b"This is not an image", "text/plain")})
    assert response.status_code == 400  # Đảm bảo phản hồi trả về HTTP 400
    assert response.json() == {"error": "Invalid image file"}  # Đảm bảo thông báo lỗi chính xác

