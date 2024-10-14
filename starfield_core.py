import ai
import starfield_structure
import pydirectinput


def generate_training_data(presets):
    embeddings = []
    starfield_presets_path = r"C:\Users\andro\OneDrive\Documents\My Games\Starfield\SFSE\Plugins\Chargen\Presets\preset.npc"
    frame = {"top": 260, "left": 1250, "width": 900, "height": 900}
    with ai.screenshot_context() as sct:
        for preset in presets:
            preset.to_file(starfield_presets_path)
            pydirectinput.press("b")  # delete
            pydirectinput.press("enter")  # F9, save is F5
            pydirectinput.press("t")  # Body
            pydirectinput.press("t")  # Face

            forward_embedding = ai.calculate_embedding(sct, frame)
            ai.show_capture(sct, frame)
            pydirectinput.mouseDown(
                button="right",
                x=frame["left"] + frame["width"],
                y=frame["top"] + frame["height"] / 2,
            )
            pydirectinput.mouseUp(
                button="right",
                x=frame["left"] + frame["width"] / 2,
                y=frame["top"] + frame["height"] / 2,
            )
            right_embedding = ai.calculate_embedding(sct, frame)
            pydirectinput.mouseDown(
                button="right", x=frame["left"], y=frame["top"] + frame["height"] / 2
            )
            pydirectinput.mouseUp(
                button="right",
                x=frame["left"] + frame["width"],
                y=frame["top"] + frame["height"] / 2,
            )
            left_embedding = ai.calculate_embedding(sct, frame)

            embedding = ai.calculate_combined_embedding(
                [forward_embedding, right_embedding, left_embedding]
            )
            embeddings.append(embedding)

            pydirectinput.press("q")  # Body
            pydirectinput.press("q")  # Presets
    return list(zip(embeddings, presets))


presets = [starfield_structure.StarfieldCharacter()]

generate_training_data(presets)
