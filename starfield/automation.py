import os
import pydirectinput

pydirectinput.PAUSE = 1

presets_path = (
    r"C:\Users\andro\OneDrive\Documents\My Games\Starfield\SFSE\Plugins\Chargen\Presets"
)

frame = {"top": 260, "left": 1250, "width": 900, "height": 900}
vertical_center = frame["top"] + frame["height"] / 2
horizontal_center = frame["left"] + frame["width"] / 2
horizontal_start = frame["left"]
horizontal_end = frame["left"] + frame["width"]


def load_preset(preset, name):
    preset.to_file(os.path.join(presets_path, name))
    pydirectinput.press("b", duration=0.1)  # delete
    pydirectinput.press("enter", duration=0.1)
    pydirectinput.press("enter", duration=0.1)  # F9, save is F5


def to_chargen_from_presets():
    pydirectinput.press("t", duration=0.1)  # Body
    pydirectinput.press("t", duration=0.1)  # Face


def to_presets_from_chargen():
    pydirectinput.press("q", duration=0.1)  # Body
    pydirectinput.press("q", duration=0.1)  # Presets


def to_left_angle():
    pydirectinput.moveTo(horizontal_start, vertical_center, duration=1)
    pydirectinput.dragTo(horizontal_end, vertical_center, button="right", duration=1)


def to_right_angle():
    pydirectinput.moveTo(horizontal_end, vertical_center, duration=1)
    pydirectinput.dragTo(horizontal_center, vertical_center, button="right", duration=1)
