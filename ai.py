import contextlib
import numpy
import cv2

# Look into https://github.com/ra1nty/DXcam/blob/main/README.md
import mss

# from keras.models import load_model

# model = load_model("facenet_keras.h5")


def __preprocess(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    image = cv2.resize(image, (160, 160))
    image = image.astype("float32") / 255.0
    image = numpy.expand_dims(image, axis=0)
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
    # return model.predict(image)
    return []


def calculate_combined_embedding(embeddings):
    return numpy.mean(embeddings, axis=0)


def show_capture(sct, frame):
    cv2.imshow("Screenshot", __screenshot(sct, frame)[0])
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()
