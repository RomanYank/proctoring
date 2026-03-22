import logging
from detectors.face_landmarker import FaceLandmarkDetector
from detectors.head_pose import HeadPoseDetector
from detectors.mouth_detector import MouthStateDetector

logger = logging.getLogger(__name__)


class FacePipeline:
    """
    Обрабатывает лицо для определения:
    - Положение точек лица (landmarks)
    - Поза головы (head pose)
    - Состояние рта (mouth state - открыт/закрыт)
    """
    
    def __init__(self, model):
        self.landmarks = FaceLandmarkDetector(model)
        self.mouth = MouthStateDetector()
        self.head_pose = HeadPoseDetector()
        self.timestamp = 0
        logger.info(f"FacePipeline initialized with model: {model}")

    def process(self, frame):
        try:
            # Получаем landmarks для лица с помощью MediaPipe
            result = self.landmarks.detect(frame, self.timestamp)
            self.timestamp += 1
            
            if not result or not result.face_landmarks or len(result.face_landmarks) == 0:
                logger.debug("No face detected in frame")
                return None

            landmarks = result.face_landmarks[0]
            
            # Определяем состояние рта
            mouth_state = self.mouth.detect(landmarks)
            logger.debug(f"Mouth state: {mouth_state.value if mouth_state else 'unknown'}")
            
            # Определяем позу головы
            head_state = self.head_pose.detect(landmarks)
            logger.debug(f"Head state: {head_state.value if head_state else 'unknown'}")

            return {
                "mouth": mouth_state,
                "head": head_state,
                "face_landmarks": landmarks,
            }
            
        except Exception as e:
            logger.exception(f"Error processing face pipeline: {e}")
            return None
