import os
import pydirectinput
import ai
import data


def generate_training_data(presets):
    embeddings = []
    with ai.screenshot_context() as sct:
        for i, preset in enumerate(presets):
            preset.to_file(os.path.join(starfield_presets_path, f"preset{i}.npc"))
            pydirectinput.press("b", duration=0.1)  # delete
            pydirectinput.press("enter", duration=0.1)
            pydirectinput.press("enter", duration=0.1)  # F9, save is F5
            pydirectinput.press("t", duration=0.1)  # Body
            pydirectinput.press("t", duration=0.1)  # Face

            ai.show_capture(sct, frame)
            forward_embedding = ai.calculate_embedding(sct, frame)
            pydirectinput.moveTo(horizontal_end, vertical_center, duration=1)
            pydirectinput.dragTo(
                horizontal_center, vertical_center, button="right", duration=1
            )
            right_embedding = ai.calculate_embedding(sct, frame)
            pydirectinput.moveTo(horizontal_start, vertical_center, duration=1)
            pydirectinput.dragTo(
                horizontal_end, vertical_center, button="right", duration=1
            )
            left_embedding = ai.calculate_embedding(sct, frame)

            embedding = ai.calculate_combined_embedding(
                [forward_embedding, right_embedding, left_embedding]
            )
            embeddings.append(embedding)

            pydirectinput.press("q", duration=0.1)  # Body
            pydirectinput.press("q", duration=0.1)  # Presets
    return list(zip(embeddings, presets))


pydirectinput.PAUSE = 1

starfield_presets_path = (
    r"C:\Users\andro\OneDrive\Documents\My Games\Starfield\SFSE\Plugins\Chargen\Presets"
)

frame = {"top": 260, "left": 1250, "width": 900, "height": 900}
vertical_center = frame["top"] + frame["height"] / 2
horizontal_center = frame["left"] + frame["width"] / 2
horizontal_start = frame["left"]
horizontal_end = frame["left"] + frame["width"]

training_data = generate_training_data([data.Character.from_random()])

print(training_data)
