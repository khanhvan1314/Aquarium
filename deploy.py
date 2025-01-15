# from fastapi import FastAPI, File, UploadFile
# from fastapi.responses import JSONResponse, StreamingResponse
# from ultralytics import YOLO
# from PIL import Image
# import io
# import cv2
# import numpy as np

# app = FastAPI()

# # Tải mô hình YOLO đã huấn luyện
# model = YOLO("best.pt")

# # API kiểm tra trạng thái
# @app.get("/")
# def read_root():
#     return {"message": "Aquarium Detection API is running!"}

# # Endpoint 1: Trả về kết quả dự đoán dưới dạng JSON
# from PIL import UnidentifiedImageError  # Thêm module này

# @app.post("/predict/json")
# async def predict_json(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents)).convert("RGB")
#     except UnidentifiedImageError:
#         return JSONResponse(content={"error": "Invalid image file"}, status_code=400)
    
#     # Tiếp tục xử lý như bình thường
#     results = model(image)
#     predictions = []
#     for result in results:
#         for box in result.boxes.data:
#             x1, y1, x2, y2, confidence, class_id = box.tolist()
#             predictions.append({
#                 "class": model.names[int(class_id)],
#                 "confidence": float(confidence),
#                 "box": [float(x1), float(y1), float(x2), float(y2)]
#             })
#     return JSONResponse(content={"predictions": predictions})


# # Endpoint 2: Trả về ảnh có bounding box
# @app.post("/predict/image")
# async def predict_image(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents)).convert("RGB")
#     except UnidentifiedImageError:
#         return JSONResponse(content={"error": "Invalid image file"}, status_code=400)

#     # Xử lý ảnh như bình thường
#     results = model(image)
#     image_np = np.array(image)
#     for result in results:
#         for box in result.boxes.data:
#             x1, y1, x2, y2, confidence, class_id = box.tolist()
#             cv2.rectangle(image_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#             cv2.putText(
#                 image_np,
#                 f"{model.names[int(class_id)]} {confidence:.2f}",
#                 (int(x1), int(y1) - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX,
#                 0.5,
#                 (0, 255, 0),
#                 1
#             )
#     image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
#     _, encoded_image = cv2.imencode('.jpg', image_np)
#     return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type="image/jpeg")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image, UnidentifiedImageError
import io
import cv2
import numpy as np

app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Thay "*" bằng danh sách các origin cụ thể để bảo mật hơn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tải mô hình YOLO đã huấn luyện
model = YOLO("best.pt")

@app.get("/")
def read_root():
    return {"message": "Aquarium Detection API is running!"}

# Endpoint 1: Trả về dự đoán dưới dạng JSON
@app.post("/predict/json")
async def predict_json(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        return JSONResponse(content={"error": "Invalid image file"}, status_code=400)
    
    results = model(image)
    predictions = []
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, confidence, class_id = box.tolist()
            predictions.append({
                "class": model.names[int(class_id)],
                "confidence": float(confidence),
                "box": [float(x1), float(y1), float(x2), float(y2)]
            })
    return JSONResponse(content={"predictions": predictions})

# Endpoint 2: Trả về ảnh có bounding box
@app.post("/predict/image")
async def predict_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
    except UnidentifiedImageError:
        return JSONResponse(content={"error": "Invalid image file"}, status_code=400)

    results = model(image)
    image_np = np.array(image)
    for result in results:
        for box in result.boxes.data:
            x1, y1, x2, y2, confidence, class_id = box.tolist()
            cv2.rectangle(image_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(
                image_np,
                f"{model.names[int(class_id)]} {confidence:.2f}",
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                1
            )
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    _, encoded_image = cv2.imencode('.jpg', image_np)
    return StreamingResponse(io.BytesIO(encoded_image.tobytes()), media_type="image/jpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
