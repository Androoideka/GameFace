import random
import json
from dataclasses import dataclass, fields
from typing import Dict
from itertools import islice
import constants
import types


def partition_iterator(iterator, size):
    return islice(iterator, size)


def random_iter():
    while True:
        yield random.random()


@dataclass
class Character:
    brow_hair_colour: constants.HairBrowColour
    eye_colour: constants.EyeColour
    hair_colour: constants.HairBrowColour
    hair: constants.HairStyle
    eyebrow: constants.BrowStyle
    eyelash: constants.EyelashStyle
    bones: Dict[constants.Demographic, types.FeatureBundle]
    sliders: Dict[constants.Demographic, types.FeatureBundle]
    body: types.Body
    head_shape: types.HeadShape
    neck: types.Neck
    chin: types.Chin
    jaw: types.Jaw
    mouth: types.Mouth
    cheeks: types.Cheeks
    nose: types.Nose
    ears: types.Ears
    eyebrows: types.Eyebrows
    eyes: types.Eyes
    forehead: types.Forehead
    skin_tone: int = 1

    @classmethod
    def from_random(cls):
        it = random_iter()
        return cls(
            brow_hair_colour=random.choice(list(constants.HairBrowColour)),
            eye_colour=random.choice(list(constants.EyeColour)),
            hair_colour=random.choice(list(constants.HairBrowColour)),
            hair=random.choice(list(constants.HairStyle)),
            eyebrow=random.choice(list(constants.BrowStyle)),
            eyelash=random.choice(list(constants.EyelashStyle)),
            skin_tone=random.randrange(0, 9),
            body=types.Body(*partition_iterator(it, len(fields(types.Body)))),
            head_shape=types.HeadShape(
                *partition_iterator(it, len(fields(types.HeadShape)))
            ),
            neck=types.Neck(*partition_iterator(it, len(fields(types.Neck)))),
            chin=types.Chin(*partition_iterator(it, len(fields(types.Chin)))),
            jaw=types.Jaw(*partition_iterator(it, len(fields(types.Jaw)))),
            mouth=types.Mouth(*partition_iterator(it, len(fields(types.Mouth)))),
            cheeks=types.Cheeks(*partition_iterator(it, len(fields(types.Cheeks)))),
            nose=types.Nose(*partition_iterator(it, len(fields(types.Nose)))),
            ears=types.Ears(*partition_iterator(it, len(fields(types.Ears)))),
            eyebrows=types.Eyebrows(
                *partition_iterator(it, len(fields(types.Eyebrows)))
            ),
            eyes=types.Eyes(*partition_iterator(it, len(fields(types.Eyes)))),
            forehead=types.Forehead(
                *partition_iterator(it, len(fields(types.Forehead)))
            ),
            bones={
                member: types.FeatureBundle(
                    *partition_iterator(it, len(fields(types.FeatureBundle)))
                )
                for member in constants.Demographic
            },
            sliders={
                member: types.FeatureBundle(
                    *partition_iterator(it, len(fields(types.FeatureBundle)))
                )
                for member in constants.Demographic
            },
        )

    @classmethod
    def from_result(cls, result):
        iterator = iter(result)
        return cls(
            skin_tone=next(iterator),
            brow_hair_colour=constants.one_hot_decode(
                constants.HairBrowColour, iterator
            ),
            eye_colour=constants.one_hot_decode(constants.EyeColour, iterator),
            hair_colour=constants.one_hot_decode(constants.HairBrowColour, iterator),
            hair=constants.one_hot_decode(constants.HairStyle, iterator),
            eyebrow=constants.one_hot_decode(constants.BrowStyle, iterator),
            eyelash=constants.one_hot_decode(constants.EyelashStyle, iterator),
            body=types.Body(*partition_iterator(iterator, len(fields(types.Body)))),
            head_shape=types.HeadShape(
                *partition_iterator(iterator, len(fields(types.HeadShape)))
            ),
            neck=types.Neck(*partition_iterator(iterator, len(fields(types.Neck)))),
            chin=types.Chin(*partition_iterator(iterator, len(fields(types.Chin)))),
            jaw=types.Jaw(*partition_iterator(iterator, len(fields(types.Jaw)))),
            mouth=types.Mouth(*partition_iterator(iterator, len(fields(types.Mouth)))),
            cheeks=types.Cheeks(
                *partition_iterator(iterator, len(fields(types.Cheeks)))
            ),
            nose=types.Nose(*partition_iterator(iterator, len(fields(types.Nose)))),
            ears=types.Ears(*partition_iterator(iterator, len(fields(types.Ears)))),
            eyebrows=types.Eyebrows(
                *partition_iterator(iterator, len(fields(types.Eyebrows)))
            ),
            eyes=types.Eyes(*partition_iterator(iterator, len(fields(types.Eyes)))),
            forehead=types.Forehead(
                *partition_iterator(iterator, len(fields(types.Forehead)))
            ),
            bones={
                demographic: types.FeatureBundle(
                    *partition_iterator(iterator, len(fields(types.FeatureBundle)))
                )
                for demographic in constants.Demographic
            },
            sliders={
                demographic: types.FeatureBundle(
                    *partition_iterator(iterator, len(fields(types.FeatureBundle)))
                )
                for demographic in constants.Demographic
            },
        )

    @classmethod
    def from_format(cls, format):
        return cls(
            brow_hair_colour=constants.HairBrowColour(format["BrowHairColor"]),
            eye_colour=constants.EyeColour(format["EyeColor"]),
            hair_colour=constants.HairBrowColour(format["HairColor"]),
            hair=constants.HairStyle(
                format["UniqueHeadPartsA"][3].removeprefix("Human_Female_Hair_")
            ),
            eyebrow=constants.BrowStyle(
                format["UniqueHeadPartsA"][6].removeprefix("Human_Female_Eyebrow_")
            ),
            eyelash=constants.EyelashStyle(
                format["UniqueHeadPartsA"][13]
                .removeprefix("Human_Female_Eyelashes_")
                .removesuffix("_Top")
            ),
            skin_tone=format["SkinTone"],
            body=types.Body.from_format(format),
            head_shape=types.HeadShape.from_bone(format["FacialBoneRegionDataA"]),
            neck=types.Neck.from_bone(format["FacialBoneRegionDataA"]),
            chin=types.Chin.from_bone(format["FacialBoneRegionDataA"]),
            jaw=types.Jaw.from_bone(format["FacialBoneRegionDataA"]),
            mouth=types.Mouth.from_bone(format["FacialBoneRegionDataA"]),
            cheeks=types.Cheeks.from_bone(format["FacialBoneRegionDataA"]),
            nose=types.Nose.from_bone(format["FacialBoneRegionDataA"]),
            ears=types.Ears.from_bone(format["FacialBoneRegionDataA"]),
            eyebrows=types.Eyebrows.from_bone(format["FacialBoneRegionDataA"]),
            eyes=types.Eyes.from_bone(format["FacialBoneRegionDataA"]),
            forehead=types.Forehead.from_bone(format["FacialBoneRegionDataA"]),
            bones={
                member: types.FeatureBundle.from_bone(
                    member, format["FacialBoneRegionDataA"]
                )
                for member in constants.Demographic
            },
            sliders={
                member: types.FeatureBundle.from_sliders(
                    member, format["FacialMorphSliderDataA"]
                )
                for member in constants.Demographic
            },
        )

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as json_file:
            return cls.from_format(json.load(json_file))

    def to_result(self):
        return (
            [self.skin_tone]
            + constants.one_hot_encode(self.brow_hair_colour)
            + constants.one_hot_encode(self.eye_colour)
            + constants.one_hot_encode(self.hair_colour)
            + constants.one_hot_encode(self.hair)
            + constants.one_hot_encode(self.eyebrow)
            + constants.one_hot_encode(self.eyelash)
            + self.body.to_result()
            + self.head_shape.to_result()
            + self.neck.to_result()
            + self.chin.to_result()
            + self.jaw.to_result()
            + self.mouth.to_result()
            + self.cheeks.to_result()
            + self.nose.to_result()
            + self.ears.to_result()
            + self.eyebrows.to_result()
            + self.eyes.to_result()
            + self.forehead.to_result()
            + [item for bone in self.bones.values() for item in bone.to_result()]
            + [item for slider in self.sliders.values() for item in slider.to_result()]
        )

    def to_format(self):
        return {
            "BrowHairColor": self.brow_hair_colour.value,
            "EyeColor": self.eye_colour.value,
            "FacialBoneRegionDataA": [
                bone
                for key, value in self.bones.items()
                if (bone := value.to_bone(key))
            ]
            + [
                value
                for value in [
                    self.head_shape.to_bone(),
                    self.neck.to_bone(),
                    self.chin.to_bone(),
                    self.jaw.to_bone(),
                    self.mouth.to_bone(),
                    self.cheeks.to_bone(),
                    self.nose.to_bone(),
                    self.ears.to_bone(),
                    self.eyebrows.to_bone(),
                    self.eyes.to_bone(),
                    self.forehead.to_bone(),
                ]
                if value
            ],
            "FacialHairColor": "",
            "FacialMorphSliderDataA": [
                item
                for key, value in self.sliders.items()
                for item in value.to_sliders(key)
            ],
            "SkinTone": self.skin_tone,
            "HairColor": self.hair_colour.value,
            "JewelryColor": "",
            "MiscHeadPartsA": [],
            "NPCFormEditorID": "",
            "PostBlendFaceCustomization": {"LayersA": []},
            "RaceFormID": "HumanRace",
            "Sex": "Female",
            "TeethCustomization": "",
            "UniqueHeadPartsA": [
                "",
                "Human_Female_Head",
                "Human_Female_RightEye",
                "Human_Female_Hair_" + self.hair.value,
                "",
                "",
                "Human_Female_Eyebrow_" + self.eyebrow.value,
                "",
                "",
                "Human_Female_Teeth",
                "",
                "",
                "Human_Female_LeftEye",
                "Human_Female_Eyelashes_" + self.eyelash.value + "_Top",
            ],
        } | self.body.to_format()

    def to_file(self, path):
        with open(path, "w") as json_file:
            json.dump(self.to_format(), json_file, indent=4)
