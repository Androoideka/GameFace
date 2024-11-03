import os
import ctypes
import pydirectinput

scale = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100
pydirectinput.PAUSE = 1

home_path = os.environ["USERPROFILE"]
presets_subpath = r"Documents\My Games\Starfield\SFSE\Plugins\Chargen\Presets"
presets_path = os.path.join(home_path, "OneDrive", presets_subpath)
if not os.path.exists(presets_path):
    presets_path = os.path.join(home_path, presets_subpath)

frame = {"top": 260, "left": 1250, "width": 900, "height": 900}
# for dpi unaware libraruies
scaled_frame = {key: value / scale for key, value in frame.items()}
vertical_center = scaled_frame["top"] + scaled_frame["height"] / 2
horizontal_center = scaled_frame["left"] + scaled_frame["width"] / 2
horizontal_start = scaled_frame["left"] - scaled_frame["width"] / 2
horizontal_end = scaled_frame["left"] + scaled_frame["width"]


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
    pydirectinput.moveTo(horizontal_center, vertical_center, duration=1.0)
    pydirectinput.dragTo(horizontal_end, vertical_center, button="right", duration=1.0)


def to_right_angle():
    pydirectinput.dragTo(
        horizontal_start, vertical_center, button="right", duration=1.0
    )
