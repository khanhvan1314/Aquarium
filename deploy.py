from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from ultralytics import YOLO
from PIL import Image
import io
import cv2
import numpy as np

app = FastAPI()

# Tải mô hình YOLO đã huấn luyện
model = YOLO("best.pt")

# API kiểm tra trạng thái
@app.get("/")
def read_root():
    return {"message": "Aquarium Detection API is running!"}

# Endpoint 1: Trả về kết quả dự đoán dưới dạng JSON
@app.post("/predict/json")
async def predict_json(file: UploadFile = File(...)):
    """
    Nhận file ảnh, phát hiện đối tượng, và trả về kết quả dưới dạng JSON.
    """
    # Đọc file ảnh
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Chạy mô hình
    results = model(image)

    # Xử lý kết quả
    predictions = []
    for result in results:
        for box in result.boxes.data:  # Lấy bounding box
            x1, y1, x2, y2, confidence, class_id = box.tolist()
            predictions.append({
                "class": model.names[int(class_id)],  # Lớp đối tượng
                "confidence": float(confidence),      # Độ tin cậy
                "box": [float(x1), float(y1), float(x2), float(y2)]  # Tọa độ bounding box
            })

    # Trả kết quả dưới dạng JSON
    return JSONResponse(content={"predictions": predictions})

# Endpoint 2: Trả về ảnh có bounding box
@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    """
    Nhận file ảnh, phát hiện đối tượng, và trả về ảnh có bounding box.
    """
    # Đọc file ảnh
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    # Chạy mô hình
    results = model(image)

    # Chuyển đổi ảnh sang numpy
    image_np = np.array(image)

    # Vẽ bounding box lên ảnh
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, confidence, class_id = box.tolist()
            # Vẽ bounding box
            cv2.rectangle(image_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Màu xanh
            cv2.putText(
                image_np,
                f"{model.names[int(class_id)]} {confidence:.2f}",
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )

    # Chuyển đổi không gian màu BGR -> RGB
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

    # Encode ảnh thành JPEG
    _, encoded_image = cv2.imencode('.jpg', image_np)

    # Trả về ảnh với bounding box dưới dạng StreamingResponse
    return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
