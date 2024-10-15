import contextlib
import numpy
import cv2
import mss  # Look into https://github.com/ra1nty/DXcam/blob/main/README.md
from deepface import DeepFace


def __preprocess(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return image


def __screenshot(sct, frame):
    screenshot = sct.grab(frame)
    image = numpy.array(screenshot)
    return __preprocess(image)


@contextlib.contextmanager
def screenshot_context():
    with mss.mss() as sct:
        yield sct


def calculate_embedding(sct, frame):
    image = __screenshot(sct, frame)
    embeddings = DeepFace.represent(
        img_path=image, model_name="Facenet512", max_faces=1
    )
    return embeddings[0]["embedding"]


def calculate_combined_embedding(embeddings):
    return numpy.mean(embeddings, axis=0)


def show_capture(sct, frame):
    cv2.imshow("Screenshot", __screenshot(sct, frame))
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()
