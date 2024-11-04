import contextlib
import numpy
import cv2
import mss  # Look into https://github.com/ra1nty/DXcam/blob/main/README.md
from deepface import DeepFace
import torch
import torch.nn
import torch.optim
from torch.utils.data import Dataset, DataLoader


class GameData(Dataset):
    def __init__(self, inputs, outputs):
        self.inputs = torch.tensor(inputs, dtype=torch.float32)
        self.outputs = torch.tensor(outputs, dtype=torch.float32)

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, index):
        return self.inputs[index], self.outputs[index]


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


def train(model, training_loader, optimizer, loss_function):
    model.train()
    total_loss = 0
    for batch_inputs, batch_outputs in training_loader:
        optimizer.zero_grad()
        outputs = model(batch_inputs)
        loss = loss_function(outputs, batch_outputs)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    total_loss /= len(training_loader.dataset)
    return total_loss


def validate(model, validation_loader, loss_function):
    model.eval()
    loss = 0
    with torch.no_grad():
        for batch_inputs, batch_outputs in validation_loader:
            outputs = model(batch_inputs)
            loss += loss_function(outputs, batch_outputs).item()
    loss /= len(validation_loader.dataset)
    return loss


def create_model(training_data, validation_data, epochs):
    training_loader = DataLoader(
        GameData(training_data[0], training_data[1]), batch_size=4, shuffle=True
    )
    validation_loader = DataLoader(
        GameData(validation_data[0], validation_data[1]), batch_size=4, shuffle=True
    )
    model = NeuralNet(len(training_data[0][0]), len(training_data[1][0]))
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_function = torch.nn.MSELoss()
    best_validation_loss = float("inf")
    for epoch in range(epochs):
        training_loss = train(model, training_loader, optimizer, loss_function)
        validation_loss = validate(model, validation_loader, loss_function)
        print(
            f"Epoch {epoch+1}/{epochs}, Training Loss: {training_loss}, Validation Loss: {validation_loss}"
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
    try:
        embeddings = DeepFace.represent(
            img_path=image, model_name="Facenet512", max_faces=1
        )
        return embeddings[0]["embedding"]
    except Exception as e:
        return None


def calculate_combined_embedding(embeddings):
    return numpy.mean(embeddings, axis=0)


def show_capture(sct, frame):
    cv2.imshow("Screenshot", __screenshot(sct, frame))
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()
