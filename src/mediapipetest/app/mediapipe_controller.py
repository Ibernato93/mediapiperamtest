import logging
from typing import Union

import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.framework.formats import detection_pb2

base_options = python.BaseOptions(model_asset_path='../app/models/mediapipe/face_landmarker.task')
options = vision.FaceLandmarkerOptions(base_options=base_options,
                                       output_face_blendshapes=True,
                                       output_facial_transformation_matrixes=True,
                                       num_faces=1)

face_detection_min_detection_confidence = 0.75
face_mesh_static_image_mode = False
face_mesh_max_num_faces = 1
face_mesh_min_detection_confidence = 0.75
face_mesh_min_tracking_confidence = 0.75

hands_static_image_mode = True
hands_max_num_hands = 2
hands_min_detection_confidence = 0.50
hands_min_tracking_confidence = 0.75

class MediaPipeController:

    def __init__(self):
        self.face_detection_processor = mp.solutions.face_detection.FaceDetection(
            min_detection_confidence=face_detection_min_detection_confidence)
        self.vision_facelandmarker = vision.FaceLandmarker.create_from_options(options)
        self.hands_processor = mp.solutions.hands.Hands(
                static_image_mode=hands_static_image_mode,
                max_num_hands=hands_max_num_hands,
                min_detection_confidence=hands_min_detection_confidence,
                min_tracking_confidence=hands_min_tracking_confidence)

    def close(self):
        """
        Releases MediaPipe resources to prevent memory leaks.
        """
        if self.face_detection_processor:
            self.face_detection_processor.close()
            self.face_detection_processor = None
        if self.vision_facelandmarker:
            self.vision_facelandmarker.close()
            self.vision_facelandmarker = None
        if self.hands_processor:
            self.hands_processor.close()
            self.hands_processor = None

    def get_first_face(self,
                       image: np.ndarray,
                       detections: detection_pb2.DetectionList = None) -> detection_pb2.Detection:
        """
        Get the first face from the image or the largest face if detections are provided.
        """
        if detections is None:
            detections = self.get_faces(image)
        if self.faces_count(detections) == 0:
            return None

        largest_face = None
        largest_area = 0

        for detection in detections.detections:
            bbox = detection.location_data.relative_bounding_box
            ih, iw, _ = image.shape
            width = int(bbox.width * iw)
            height = int(bbox.height * ih)
            area = width * height

            if area > largest_area:
                largest_area = area
                largest_face = detection

        return largest_face

    def faces_count(self,
                    detections: detection_pb2.DetectionList):
        if detections is None or detections.detections is None:
            return 0
        return len(detections.detections)

    def get_faces(self, image: np.ndarray) -> Union[detection_pb2.DetectionList, None]:
    """
    Face detection with MediaPipe
    @return results: results.detections is a list of rectangles, each containing a face
    """
    try:
        return self.face_detection_processor.process(image)
    except Exception as e:
        logging.exception("During face detection: {}".format(str(e)))
        return None
