from dataclasses import dataclass, fields
from enum import Enum
from typing import Type
from starfield import constants


@dataclass
class Morph:
    def to_result(self):
        return [getattr(self, field.name) for field in fields(self)]


@dataclass
class FeatureBundle(Morph):
    neck: float = 0.0
    cheeks: float = 0.0
    jaw: float = 0.0
    chin: float = 0.0
    ears: float = 0.0
    eyes: float = 0.0
    forehead: float = 0.0
    mouth: float = 0.0
    nose: float = 0.0

    @classmethod
    def from_json_morphs(cls, demographic, morphs):
        dict = morphs.get(str(demographic.value), {})
        mapping = {k.lower(): v for k, v in dict.items()}
        return cls(**mapping)

    @classmethod
    def from_json_blends(cls, demographic, blends):
        mapping = {
            k.split("_")[-1].lower(): v
            for k, v in blends.items()
            if k.startswith(demographic.name)
        }
        return cls(**mapping)

    @classmethod
    def from_bone(cls, demographic, bones):
        bone = next(
            (bone for bone in bones if bone["RegionID"] == demographic.value),
            {"SlidersA": []},
        )
        mapping = {
            slider["GroupName"].lower(): slider["Value"] for slider in bone["SlidersA"]
        }
        return cls(**mapping)

    @classmethod
    def from_sliders(cls, demographic, sliders):
        mapping = {
            slider["Name"].split("_")[-1].lower(): slider["Value"]
            for slider in sliders
            if slider["Name"].startswith(demographic.name)
        }
        return cls(**mapping)

    def to_sliders(self, demographic: constants.Demographic):
        dict = {
            field.name.capitalize(): getattr(self, field.name) for field in fields(self)
        }
        should_write = any(value != 0.0 for value in dict.values())
        return (
            [
                {"Name": demographic.name + "_" + key, "Value": value}
                for key, value in dict.items()
            ]
            if should_write
            else []
        )

    def to_bone(self, demographic: constants.Demographic):
        dict = {
            field.name.capitalize(): getattr(self, field.name) for field in fields(self)
        }
        should_write = any(value != 0.0 for value in dict.values())
        return (
            {
                "RegionID": demographic.value,
                "SlidersA": [
                    {"GroupName": key, "ID": 0, "Value": value}
                    for key, value in dict.items()
                ],
            }
            if should_write
            else {}
        )


@dataclass
class Sliders(Morph):
    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        raise NotImplementedError

    @classmethod
    def get_region(cls) -> int:
        raise NotImplementedError

    @classmethod
    def from_json(cls, sliders):
        mapping = {
            member.name: sliders[str(member.value)]
            for member in cls.get_enum_type()
            if str(member.value) in sliders
        }
        return cls(**mapping)

    @classmethod
    def from_bone(cls, bones):
        bone = next(
            (bone for bone in bones if bone["RegionID"] == cls.get_region()),
            {"SlidersA": []},
        )
        mapping = {
            cls.get_enum_type()(slider["ID"]).name: slider["Value"]
            for slider in bone["SlidersA"]
            if slider["ID"] != 0
        }
        return cls(**mapping)

    def to_bone(self):
        dict = {field.name: getattr(self, field.name) for field in fields(self)}
        should_write = any(value != 0.0 for value in dict.values())
        return (
            {
                "RegionID": self.get_region(),
                "SlidersA": [
                    {
                        "GroupName": "",
                        "ID": self.get_enum_type()[key].value,
                        "Value": value,
                    }
                    for key, value in dict.items()
                ],
            }
            if should_write
            else {}
        )


@dataclass
class HeadShape(Sliders):
    square: float = 0.0
    round: float = 0.0
    narrow: float = 0.0
    wide: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.HeadShapeSliders

    @classmethod
    def get_region(cls) -> int:
        return 23


@dataclass
class Neck(Sliders):
    wattle_in_out: float = 0.0
    narrow_wide: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.NeckSliders

    @classmethod
    def get_region(cls) -> int:
        return 29


@dataclass
class Chin(Sliders):
    narrow_wide: float = 0.0
    back_forward: float = 0.0
    down_up: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.ChinSliders

    @classmethod
    def get_region(cls) -> int:
        return 33


@dataclass
class Jaw(Sliders):
    narrow_wide: float = 0.0
    back_forward: float = 0.0
    down_up: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.JawSliders

    @classmethod
    def get_region(cls) -> int:
        return 37


@dataclass
class Mouth(Sliders):
    underbite_overbite: float = 0.0
    scale_down_up: float = 0.0
    left_right: float = 0.0
    down_up: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.MouthSliders

    @classmethod
    def get_region(cls) -> int:
        return 41


@dataclass
class Cheeks(Sliders):
    down_up: float = 0.0
    scale_down_up: float = 0.0
    narrow_wide: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.CheeksSliders

    @classmethod
    def get_region(cls) -> int:
        return 46


@dataclass
class Nose(Sliders):
    nose_tip_down_up: float = 0.0
    short_long: float = 0.0
    narrow_wide: float = 0.0
    back_forward: float = 0.0
    down_up: float = 0.0
    nostril_up_down: float = 0.0
    nostrills_in_out: float = 0.0
    rigde_narrow_wide: float = 0.0
    ridge_in_out: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.NoseSliders

    @classmethod
    def get_region(cls) -> int:
        return 50


@dataclass
class Ears(Sliders):
    narrow_wide: float = 0.0
    back_forward: float = 0.0
    down_up: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.EarsSliders

    @classmethod
    def get_region(cls) -> int:
        return 56


@dataclass
class Eyebrows(Sliders):
    narrow_wide: float = 0.0
    back_forward: float = 0.0
    down_up: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.EyebrowsSliders

    @classmethod
    def get_region(cls) -> int:
        return 60


@dataclass
class Eyes(Sliders):
    narrow_wide: float = 0.0
    scale_down_up: float = 0.0
    back_forward: float = 0.0
    down_up: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.EyesSliders

    @classmethod
    def get_region(cls) -> int:
        return 64


@dataclass
class Forehead(Sliders):
    narrow_wide: float = 0.0
    back_forward: float = 0.0

    @classmethod
    def get_enum_type(cls) -> Type[Enum]:
        return constants.ForeheadSliders

    @classmethod
    def get_region(cls) -> int:
        return 71


@dataclass
class Body(Morph):
    thin: float = 0.0
    muscular: float = 0.0
    heavy: float = 0.0
    head: float = 0.0
    upper_torso: float = 0.0
    arms: float = 0.0
    lower_torso: float = 0.0
    legs: float = 0.0

    @classmethod
    def from_format(cls, format):
        values = (
            list(format["MorphWeights"].values()) + format["BodyMorphRegionValuesA"]
        )
        return cls(*values)

    @classmethod
    def from_json(cls, format):
        values = list(format["Weight"].values()) + format.get(
            "BodyMorphRegionValues", [0] * 5
        )
        return cls(*values)

    def to_format(self):
        return {
            "BodyMorphRegionValuesA": [
                self.head,
                self.upper_torso,
                self.arms,
                self.lower_torso,
                self.legs,
            ],
            "MorphWeights": {"x": self.thin, "y": self.muscular, "z": self.heavy},
        }
