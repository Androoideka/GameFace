import os
import constants
import data

directory = input("Please enter path that contains presets: ")

for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".npc") or file.endswith(".json"):
            preset = data.Character.from_file(os.path.join(root, file))
            values = {
                "neck": 0.0,
                "cheeks": 0.0,
                "jaw": 0.0,
                "chin": 0.0,
                "ears": 0.0,
                "eyes": 0.0,
                "forehead": 0.0,
                "mouth": 0.0,
                "nose": 0.0,
            }
            for demographic in constants.Demographic:
                values["neck"] += preset.bones[demographic].neck
                values["cheeks"] += preset.bones[demographic].cheeks
                values["jaw"] += preset.bones[demographic].jaw
                values["chin"] += preset.bones[demographic].chin
                values["ears"] += preset.bones[demographic].ears
                values["eyes"] += preset.bones[demographic].eyes
                values["forehead"] += preset.bones[demographic].forehead
                values["mouth"] += preset.bones[demographic].mouth
                values["nose"] += preset.bones[demographic].nose
            if any([val > 1.0001 for val in values.values()]):
                print("\n")
                print(file)
                print(values)
