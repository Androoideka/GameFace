import os
import ai
from starfield import automation, data


def generate_training_data(presets):
    embeddings = []
    with ai.screenshot_context() as sct:
        for i, preset in enumerate(presets):
            automation.load_preset(preset, f"preset{i}.npc")
            automation.to_chargen_from_presets()

            ai.show_capture(sct, automation.frame)
            forward_embedding = ai.calculate_embedding(sct, automation.frame)
            automation.to_right_angle()
            right_embedding = ai.calculate_embedding(sct, automation.frame)
            automation.to_left_angle()
            left_embedding = ai.calculate_embedding(sct, automation.frame)

            embedding = ai.calculate_combined_embedding(
                [forward_embedding, right_embedding, left_embedding]
            )
            embeddings.append(embedding)

            automation.to_presets_from_chargen()
    return list(zip(embeddings, presets))


training_data = generate_training_data([data.Character.from_random()])

print(training_data)
