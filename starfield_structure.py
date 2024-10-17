import starfield_constants
import random
import json


def one_hot_encode(index, length):
    one_hot = [0] * length
    one_hot[index] = 1
    return one_hot


def one_hot_decode(it, length):
    one_hot_vector = [next(it) for _ in range(length)]
    return one_hot_vector.index(1)


class StarfieldCharacter:
    def __init__(
        self,
        brow_hair_colour,
        eye_colour,
        hair_colour,
        skin_tone,
        hair,
        eyebrow,
        feature_bones,
        additional_bones,
        sliders,
    ):
        self.brow_hair_colour = brow_hair_colour
        self.eye_colour = eye_colour
        self.hair_colour = hair_colour
        self.skin_tone = skin_tone
        self.hair = hair
        self.eyebrow = eyebrow
        self.feature_bones = feature_bones
        self.additional_bones = additional_bones
        self.sliders = sliders

    @classmethod
    def from_random(cls):
        brow_hair_colour = random.choice(starfield_constants.hair_brow_colours)
        eye_colour = random.choice(starfield_constants.eye_colours)
        hair_colour = random.choice(starfield_constants.hair_brow_colours)
        skin_tone = random.choice(starfield_constants.skin_tones)
        hair = random.choice(starfield_constants.hair_styles)
        eyebrow = random.choice(starfield_constants.brow_styles)
        feature_bones = {
            region: {
                feature: random.random() for feature in starfield_constants.features
            }
            for region in starfield_constants.feature_regions
        }
        additional_bones = {
            region: {id: random.random() for id in ids}
            for region, ids in starfield_constants.additional_regions.items()
        }
        sliders = {
            variation + feature: random.random()
            for variation in starfield_constants.variations
            for feature in starfield_constants.features
        }
        return cls(
            brow_hair_colour,
            eye_colour,
            hair_colour,
            skin_tone,
            hair,
            eyebrow,
            feature_bones,
            additional_bones,
            sliders,
        )

    @classmethod
    def from_result(cls, result):
        it = iter(result)
        brow_hair_colour = starfield_constants.hair_brow_colours[
            one_hot_decode(it, len(starfield_constants.hair_brow_colours))
        ]
        eye_colour = starfield_constants.eye_colours[
            one_hot_decode(it, len(starfield_constants.eye_colours))
        ]
        hair_colour = starfield_constants.hair_brow_colours[
            one_hot_decode(it, len(starfield_constants.hair_brow_colours))
        ]
        skin_tone = starfield_constants.skin_tones[
            one_hot_decode(it, len(starfield_constants.skin_tones))
        ]
        hair = starfield_constants.hair_styles[
            one_hot_decode(it, len(starfield_constants.hair_styles))
        ]
        eyebrow = starfield_constants.brow_styles[
            one_hot_decode(it, len(starfield_constants.brow_styles))
        ]
        feature_bones = {
            region: {feature: next(it) for feature in starfield_constants.features}
            for region in starfield_constants.feature_regions
        }
        additional_bones = {
            region: {id: next(it) for id in ids}
            for region, ids in starfield_constants.additional_regions.items()
        }
        sliders = {
            variation + "_" + feature: next(it)
            for variation in starfield_constants.variations
            for feature in starfield_constants.features
        }
        return cls(
            brow_hair_colour,
            eye_colour,
            hair_colour,
            skin_tone,
            hair,
            eyebrow,
            feature_bones,
            additional_bones,
            sliders,
        )

    @classmethod
    def from_format(cls, format):
        brow_hair_colour = format["BrowHairColor"]
        eye_colour = format["EyeColor"]
        hair_colour = format["HairColor"]
        skin_tone = format["SkinTone"]
        hair = format["UniqueHeadPartsA"][3].removeprefix("Human_Female_Hair_")
        eyebrow = format["UniqueHeadPartsA"][6].removeprefix("Human_Female_Eyebrow_")
        feature_bones = {
            item["RegionID"]: {
                nested_item["GroupName"]: nested_item["Value"]
                for nested_item in item["SlidersA"]
            }
            for item in format["FacialBoneRegionDataA"]
            if item["RegionID"] in starfield_constants.feature_regions
        }
        additional_bones = {
            item["RegionID"]: {
                nested_item["ID"]: nested_item["Value"]
                for nested_item in item["SlidersA"]
            }
            for item in format["FacialBoneRegionDataA"]
            if item["RegionID"] not in starfield_constants.feature_regions
        }
        sliders = {
            item["Name"].removeprefix("female_"): item["Value"]
            for item in format["FacialMorphSliderDataA"]
        }
        return cls(
            brow_hair_colour,
            eye_colour,
            hair_colour,
            skin_tone,
            hair,
            eyebrow,
            feature_bones,
            additional_bones,
            sliders,
        )

    @classmethod
    def from_file(cls, path):
        with open(path, "r") as json_file:
            return cls.from_format(json.load(json_file))

    def to_result(self):
        return (
            one_hot_encode(
                starfield_constants.hair_brow_colours.index(self.brow_hair_colour),
                len(starfield_constants.hair_brow_colours),
            )
            + one_hot_encode(
                starfield_constants.eye_colours.index(self.eye_colour),
                len(starfield_constants.eye_colours),
            )
            + one_hot_encode(
                starfield_constants.hair_brow_colours.index(self.hair_colour),
                len(starfield_constants.hair_brow_colours),
            )
            + one_hot_encode(
                starfield_constants.skin_tones.index(self.skin_tone),
                len(starfield_constants.skin_tones),
            )
            + one_hot_encode(
                starfield_constants.hair_styles.index(self.hair),
                len(starfield_constants.hair_styles),
            )
            + one_hot_encode(
                starfield_constants.brow_styles.index(self.eyebrow),
                len(starfield_constants.brow_styles),
            )
            + [
                self.feature_bones[region][feature]
                for region in starfield_constants.feature_regions
                for feature in starfield_constants.features
            ]
            + [
                self.additional_bones[region][id]
                for region, ids in starfield_constants.additional_regions.items()
                for id in ids
            ]
            + [
                self.sliders[variation + "_" + feature]
                for variation in starfield_constants.variations
                for feature in starfield_constants.features
            ]
        )

    def to_format(self):
        return {
            "BodyMorphRegionValuesA": [],
            "BrowHairColor": self.brow_hair_colour,
            "EyeColor": self.eye_colour,
            "FacialBoneRegionDataA": [
                {
                    "RegionID": region,
                    "SlidersA": [
                        {"GroupName": feature, "ID": 0, "Value": value}
                        for feature, value in features.items()
                    ],
                }
                for region, features in self.feature_bones.items()
            ]
            + [
                {
                    "RegionID": region,
                    "SlidersA": [
                        {"GroupName": "", "ID": id, "Value": value}
                        for id, value in ids.items()
                    ],
                }
                for region, ids in self.additional_bones.items()
            ],
            "FacialHairColor": "",
            "FacialMorphSliderDataA": [
                {"Name": "female_" + slider, "Value": value}
                for slider, value in self.sliders.items()
            ],
            "HairColor": self.hair_colour,
            "JewelryColor": "",
            "MiscHeadPartsA": [],
            "MorphWeights": {"x": 0.0, "y": 0.0, "z": 0.0},
            "NPCFormEditorID": "",
            "PostBlendFaceCustomization": {"LayersA": []},
            "RaceFormID": "HumanRace",
            "Sex": "Female",
            "SkinTone": self.skin_tone,
            "TeethCustomization": "",
            "UniqueHeadPartsA": [
                "",
                "Human_Female_Head",
                "Human_Female_RightEye",
                "Human_Female_Hair_" + self.hair,
                "",
                "",
                "Human_Female_Eyebrow_" + self.eyebrow,
                "",
                "",
                "Human_Female_Teeth",
                "",
                "",
                "Human_Female_LeftEye",
                "Human_Female_Eyelashes_01_Top",
            ],
        }

    def to_file(self, path):
        with open(path, "w") as json_file:
            json.dump(self.to_format(), json_file, indent=4)
