import contextlib
import numpy
import cv2
import mss  # Look into https://github.com/ra1nty/DXcam/blob/main/README.md
from deepface import DeepFace
import torch
import torch.nn
import torch.optim


class NeuralNet(torch.nn.Module):
    def __init__(self, input, output):
        super(NeuralNet, self).__init__()
        self.shared_layer = torch.nn.Linear(input, 256)
        self.relu = torch.nn.ReLU()
        self.final_layer = torch.nn.Linear(256, output)

    def forward(self, x):
        x = self.relu(self.shared_layer(x))
        output = self.final_layer(x)
        return output


def train(training_pairs, validation_pairs, epochs):
    (example_input, example_result) = training_pairs[0]
    model = NeuralNet(len(example_input), len(example_result))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.MSELoss()
    best_validation_loss = float("inf")
    for epoch in range(epochs):
        model.train()
        for input, result in training_pairs:
            optimizer.zero_grad()
            print(input)
            output = model(input)
            training_loss = loss_fn(output, result)
            training_loss.backward()
            optimizer.step()

        model.eval()
        validation_loss = 0
        with torch.no_grad():
            for input, result in validation_pairs:
                output = model(input)
                validation_loss += loss_fn(output, result).item()
        validation_loss /= len(validation_pairs)

        print(
            f"Epoch {epoch+1}/{epochs}, Training Loss: {training_loss.item()}, Validation Loss: {validation_loss}"
        )
        if validation_loss < best_validation_loss:
            best_validation_loss = validation_loss
            torch.save(model.state_dict(), "model.pth")
            print(f"Best model saved with validation loss: {validation_loss}")


def test(input):
    model = NeuralNet()
    model.load_state_dict(torch.load("model.pth"))
    model.eval()  # Set the model to evaluation mode
    with torch.no_grad():
        predictions = model(input)
        return predictions


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
