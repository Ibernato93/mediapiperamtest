import gc

import cv2
import uvicorn
from fastapi import FastAPI
from mediapipe_controller import MediaPipeController

app = FastAPI()

@app.get("/process_frame/{number}")
async def process_frame(number: int):
    print(f"***** Process {number} test *****")
    mediapipe_ctrl = MediaPipeController()
    image = cv2.imread("test_image.jpeg")
    for i in range(0, number + 1):
        mediapipe_ctrl.get_first_face(image)
        mediapipe_ctrl.hands_processor.process(image)
    mediapipe_ctrl.close()
    mediapipe_ctrl = None
    gc.collect()
    return {"status": "Process finished"}

@app.get("/status")
async def status():
    return {"status": "Service is up"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)
