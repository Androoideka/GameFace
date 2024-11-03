import numpy
import ai
import torch
from starfield import automation, data


def create_input_result(presets):
    embeddings = {}
    results = {key: numpy.array(value.to_result()) for key, value in presets.items()}
    with ai.screenshot_context() as sct:
        for i, preset in enumerate(presets.values()):
            automation.load_preset(preset, f"preset{i}.npc")
            automation.to_chargen_from_presets()

            embedding = ai.calculate_embedding(sct, automation.frame)
            embeddings[f"{i}-embedding"] = embedding

            automation.to_presets_from_chargen()
    return {**embeddings, **results}


def generate_data(num, path):
    presets = {f"{i}-preset": data.Character.from_random() for i in range(num)}
    pairs = create_input_result(presets)
    numpy.savez_compressed(path, **pairs)


def load_data(path):
    pairs = numpy.load(path)
    return [
        (
            torch.tensor(pairs[f"{i}-preset"], dtype=torch.float32),
            torch.tensor(pairs[f"{i}-embedding"], dtype=torch.float32),
        )
        for i in range(len(pairs) // 2)
    ]


generate_data(20, "training.npz")

generate_data(5, "validation.npz")

ai.train(load_data("training.npz"), load_data("validation.npz"), 10)

# ai.test()
