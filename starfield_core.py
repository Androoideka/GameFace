import ai
import starfield_structure
import pydirectinput


def generate_training_data(presets):
    embeddings = []
    starfield_presets_path = r"C:\Users\andro\OneDrive\Documents\My Games\Starfield\SFSE\Plugins\Chargen\Presets\preset.npc"
    frame = {"top": 260, "left": 1250, "width": 900, "height": 900}
    vertical_center = frame["top"] + frame["height"] / 2
    horizontal_center = frame["left"] + frame["width"] / 2
    horizontal_start = frame["left"]
    horizontal_end = frame["left"] + frame["width"]
    with ai.screenshot_context() as sct:
        for preset in presets:
            preset.to_file(starfield_presets_path)
            print("Beginning input")
            pydirectinput.press("b")  # delete
            pydirectinput.press("enter")
            pydirectinput.press("enter")  # F9, save is F5
            pydirectinput.press("t")  # Body
            pydirectinput.press("t")  # Face

            # ai.show_capture(sct, frame)
            forward_embedding = ai.calculate_embedding(sct, frame)
            pydirectinput.moveTo(horizontal_end, vertical_center)
            pydirectinput.dragTo(horizontal_center, vertical_center, button="right")
            right_embedding = ai.calculate_embedding(sct, frame)
            pydirectinput.moveTo(horizontal_start, vertical_center)
            pydirectinput.dragTo(horizontal_end, vertical_center, button="right")
            left_embedding = ai.calculate_embedding(sct, frame)

            embedding = ai.calculate_combined_embedding(
                [forward_embedding, right_embedding, left_embedding]
            )
            embeddings.append(embedding)

            pydirectinput.press("q")  # Body
            pydirectinput.press("q")  # Presets
    return list(zip(embeddings, presets))


pydirectinput.PAUSE = 1

presets = [starfield_structure.StarfieldCharacter()]

training_data = generate_training_data(presets)

print(training_data)
