import numpy
import ai
from starfield import automation, data


def create_input_result(presets):
    embeddings = {}
    with ai.screenshot_context() as sct:
        for i, preset in enumerate(presets.values()):
            automation.load_preset(preset, f"preset{i}.npc")
            automation.to_chargen_from_presets()

            embedding = ai.calculate_embedding(sct, automation.frame)
            embeddings[f"{i}-embedding"] = embedding

            automation.to_presets_from_chargen()
    return {**embeddings, **presets}


def generate_data(num, path):
    presets = {
        f"{i}-preset": numpy.array(data.Character.from_random()) for i in range(num)
    }
    pairs = create_input_result(presets)
    numpy.savez_compressed(path, **pairs)


def load_data(path):
    pairs = numpy.load(path)
    return [
        (pairs[f"{i}-preset"], pairs[f"{i}-embedding"]) for i in range(len(pairs) // 2)
    ]


generate_data(20, "training.npz")

generate_data(5, "validation.npz")
