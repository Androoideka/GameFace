import os
import uuid
import numpy
import ai
from starfield import automation, data


def get_embedding(sct, preset):
    automation.show_preset(preset, uuid.uuid4().hex)
    automation.to_chargen_from_presets()
    embedding = ai.calculate_embedding(sct, automation.frame)
    automation.to_presets_from_chargen()
    return embedding


def get_embeddings(presets):
    with ai.screenshot_context() as sct:
        return [get_embedding(sct, preset) for preset in presets]


def load_presets(directory):
    return [
        data.Character.from_file(os.path.join(root, file))
        for root, _, files in os.walk(directory)
        for file in files
        if file.endswith(".npc") or file.endswith(".json")
    ]


def generate_presets(num):
    return [data.Character.from_random() for i in range(num)]


def save_data(presets, path):
    embeddings = get_embeddings(presets)
    results = [preset.to_result() for preset in presets]
    numpy.savez_compressed(path, results=results, embeddings=embeddings)


def load_data(path):
    data = numpy.load(path)
    return (data["embeddings"], data["results"])


loaded_presets = load_presets("input")
generated_training_presets = generate_presets(4)
generated_validation_presets = generate_presets(4)
save_data(generated_training_presets, "output/training.npz")
save_data(generated_validation_presets, "output/validation.npz")

ai.create_model(
    load_data("output/training.npz"), load_data("output/validation.npz"), 10
)

# ai.test()
