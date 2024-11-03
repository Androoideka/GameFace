import random
import json
import utilities
from dataclasses import dataclass, fields
from typing import Dict
from starfield import constants, classes


@dataclass
class Character:
    brow_hair_colour: constants.HairBrowColour
    eye_colour: constants.EyeColour
    hair_colour: constants.HairBrowColour
    hair: constants.HairStyle
    eyebrow: constants.BrowStyle
    eyelash: constants.EyelashStyle
    bones: Dict[constants.Demographic, classes.FeatureBundle]
    sliders: Dict[constants.Demographic, classes.FeatureBundle]
    body: classes.Body
    head_shape: classes.HeadShape
    neck: classes.Neck
    chin: classes.Chin
    jaw: classes.Jaw
    mouth: classes.Mouth
    cheeks: classes.Cheeks
    nose: classes.Nose
    ears: classes.Ears
    eyebrows: classes.Eyebrows
    eyes: classes.Eyes
    forehead: classes.Forehead
    skin_tone: int = 1

    @classmethod
    def from_random(cls):
        return cls(
            brow_hair_colour=random.choice(list(constants.HairBrowColour)),
            eye_colour=random.choice(list(constants.EyeColour)),
            hair_colour=random.choice(list(constants.HairBrowColour)),
            hair=random.choice(list(constants.HairStyle)),
            eyebrow=random.choice(list(constants.BrowStyle)),
            eyelash=random.choice(list(constants.EyelashStyle)),
            skin_tone=random.randrange(0, 9),
            body=classes.Body(
                *[random.random() for _ in range(len(fields(classes.Body)))]
            ),
            head_shape=classes.HeadShape(
                *[random.random() for _ in range(len(fields(classes.HeadShape)))]
            ),
            neck=classes.Neck(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Neck)))]
            ),
            chin=classes.Chin(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Chin)))]
            ),
            jaw=classes.Jaw(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Jaw)))]
            ),
            mouth=classes.Mouth(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Mouth)))]
            ),
            cheeks=classes.Cheeks(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Cheeks)))]
            ),
            nose=classes.Nose(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Nose)))]
            ),
            ears=classes.Ears(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Ears)))]
            ),
            eyebrows=classes.Eyebrows(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Eyebrows)))]
            ),
            eyes=classes.Eyes(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Eyes)))]
            ),
            forehead=classes.Forehead(
                *[random.uniform(-1, 1) for _ in range(len(fields(classes.Forehead)))]
            ),
            bones={
                member: classes.FeatureBundle(*features)
                for member, features in zip(
                    constants.Demographic,
                    utilities.transpose(
                        [
                            utilities.random_sum(len(constants.Demographic))
                            for _ in fields(classes.FeatureBundle)
                        ]
                    ),
                )
            },
            sliders={
                member: classes.FeatureBundle(*features)
                for member, features in zip(
                    constants.Demographic,
                    utilities.transpose(
                        [
                            utilities.random_sum(len(constants.Demographic))
                            for _ in fields(classes.FeatureBundle)
                        ]
                    ),
                )
            },
        )

    @classmethod
    def from_result(cls, result):
        iterator = iter(result)
        return cls(
            skin_tone=next(iterator),
            brow_hair_colour=utilities.one_hot_decode(
                constants.HairBrowColour, iterator
            ),
            eye_colour=utilities.one_hot_decode(constants.EyeColour, iterator),
            hair_colour=utilities.one_hot_decode(constants.HairBrowColour, iterator),
            hair=utilities.one_hot_decode(constants.HairStyle, iterator),
            eyebrow=utilities.one_hot_decode(constants.BrowStyle, iterator),
            eyelash=utilities.one_hot_decode(constants.EyelashStyle, iterator),
            body=classes.Body(
                *utilities.partition_iterator(iterator, len(fields(classes.Body)))
            ),
            head_shape=classes.HeadShape(
                *utilities.partition_iterator(iterator, len(fields(classes.HeadShape)))
            ),
            neck=classes.Neck(
                *utilities.partition_iterator(iterator, len(fields(classes.Neck)))
            ),
            chin=classes.Chin(
                *utilities.partition_iterator(iterator, len(fields(classes.Chin)))
            ),
            jaw=classes.Jaw(
                *utilities.partition_iterator(iterator, len(fields(classes.Jaw)))
            ),
            mouth=classes.Mouth(
                *utilities.partition_iterator(iterator, len(fields(classes.Mouth)))
            ),
            cheeks=classes.Cheeks(
                *utilities.partition_iterator(iterator, len(fields(classes.Cheeks)))
            ),
            nose=classes.Nose(
                *utilities.partition_iterator(iterator, len(fields(classes.Nose)))
            ),
            ears=classes.Ears(
                *utilities.partition_iterator(iterator, len(fields(classes.Ears)))
            ),
            eyebrows=classes.Eyebrows(
                *utilities.partition_iterator(iterator, len(fields(classes.Eyebrows)))
            ),
            eyes=classes.Eyes(
                *utilities.partition_iterator(iterator, len(fields(classes.Eyes)))
            ),
            forehead=classes.Forehead(
                *utilities.partition_iterator(iterator, len(fields(classes.Forehead)))
            ),
            bones={
                demographic: classes.FeatureBundle(
                    *utilities.partition_iterator(
                        iterator, len(fields(classes.FeatureBundle))
                    )
                )
                for demographic in constants.Demographic
            },
            sliders={
                demographic: classes.FeatureBundle(
                    *utilities.partition_iterator(
                        iterator, len(fields(classes.FeatureBundle))
                    )
                )
                for demographic in constants.Demographic
            },
        )

    @classmethod
    def from_json(cls, format):
        return cls(
            brow_hair_colour=constants.HairBrowColour(format["EyebrowColor"]),
            eye_colour=constants.EyeColour(format["EyeColor"]),
            hair_colour=constants.HairBrowColour(format["HairColor"]),
            hair=constants.HairStyle.Straight_Bob,
            eyebrow=constants.BrowStyle.Standard,
            eyelash=constants.EyelashStyle.Style1,
            skin_tone=format["SkinTone"],
            body=classes.Body.from_json(format),
            head_shape=classes.HeadShape.from_json(format["AdditionalSliders"]),
            neck=classes.Neck.from_json(format["AdditionalSliders"]),
            chin=classes.Chin.from_json(format["AdditionalSliders"]),
            jaw=classes.Jaw.from_json(format["AdditionalSliders"]),
            mouth=classes.Mouth.from_json(format["AdditionalSliders"]),
            cheeks=classes.Cheeks.from_json(format["AdditionalSliders"]),
            nose=classes.Nose.from_json(format["AdditionalSliders"]),
            ears=classes.Ears.from_json(format["AdditionalSliders"]),
            eyebrows=classes.Eyebrows.from_json(format["AdditionalSliders"]),
            eyes=classes.Eyes.from_json(format["AdditionalSliders"]),
            forehead=classes.Forehead.from_json(format["AdditionalSliders"]),
            bones={
                member: classes.FeatureBundle.from_json_morphs(
                    member, format.get("Morphs", {})
                )
                for member in constants.Demographic
            },
            sliders={
                member: classes.FeatureBundle.from_json_blends(
                    member, format["ShapeBlendData"]
                )
                for member in constants.Demographic
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
            body=classes.Body.from_format(format),
            head_shape=classes.HeadShape.from_bone(format["FacialBoneRegionDataA"]),
            neck=classes.Neck.from_bone(format["FacialBoneRegionDataA"]),
            chin=classes.Chin.from_bone(format["FacialBoneRegionDataA"]),
            jaw=classes.Jaw.from_bone(format["FacialBoneRegionDataA"]),
            mouth=classes.Mouth.from_bone(format["FacialBoneRegionDataA"]),
            cheeks=classes.Cheeks.from_bone(format["FacialBoneRegionDataA"]),
            nose=classes.Nose.from_bone(format["FacialBoneRegionDataA"]),
            ears=classes.Ears.from_bone(format["FacialBoneRegionDataA"]),
            eyebrows=classes.Eyebrows.from_bone(format["FacialBoneRegionDataA"]),
            eyes=classes.Eyes.from_bone(format["FacialBoneRegionDataA"]),
            forehead=classes.Forehead.from_bone(format["FacialBoneRegionDataA"]),
            bones={
                member: classes.FeatureBundle.from_bone(
                    member, format["FacialBoneRegionDataA"]
                )
                for member in constants.Demographic
            },
            sliders={
                member: classes.FeatureBundle.from_sliders(
                    member, format["FacialMorphSliderDataA"]
                )
                for member in constants.Demographic
            },
        )

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as file:
            contents = json.load(file)
            if path.endswith(".npc"):
                return cls.from_format(contents)
            elif path.endswith(".json"):
                return cls.from_json(contents)

    def __getitem__(self, demographic):
        return (self.bones[demographic], self.sliders[demographic])

    def to_result(self):
        return (
            [self.skin_tone]
            + utilities.one_hot_encode(self.brow_hair_colour)
            + utilities.one_hot_encode(self.eye_colour)
            + utilities.one_hot_encode(self.hair_colour)
            + utilities.one_hot_encode(self.hair)
            + utilities.one_hot_encode(self.eyebrow)
            + utilities.one_hot_encode(self.eyelash)
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
