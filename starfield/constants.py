from enum import Enum


class Demographic(Enum):
    female_eu_yo1 = 17
    female_eu_md2 = 1
    female_eu_ol1 = 3
    female_as_yo1 = 19
    female_as_ol1 = 11
    female_as_md1 = 5
    female_af_yo1 = 13
    female_af_ol1 = 15
    female_af_md1 = 9


class EyeColour(Enum):
    Dead = "Dead"
    Grey = "Grey"
    Sulfur = "Sulfur"
    Green = "Green"
    Copper = "Copper"
    Hazel = "Hazel"
    Blue = "Blue"
    RedDevil = "RedDevil"
    Red = "Red"
    Iron = "Iron"
    Brown = "Brown"
    BrownDark = "BrownDark"


class HairBrowColour(Enum):
    White = "White"
    Platinum = "Platinum"
    Grey = "Grey"
    Blonde = "Blonde"
    DirtyBlonde = "DirtyBlonde"
    Amber = "Amber"
    Copper = "Copper"
    Ruby = "Ruby"
    SaltAndBrown = "SaltAndBrown"
    Brown = "Brown"
    SaltAndPepper = "SaltAndPepper"
    BlackBrown = "BlackBrown"
    Auburn = "Auburn"
    Black = "Black"
    Jet = "Jet"
    TealBlonde = "TealBlonde"
    Yellow = "Yellow"
    Violet = "Violet"
    Flame = "Flame"
    Blue = "Blue"
    Fuchsia = "Fuchsia"
    AquaPurple = "AquaPurple"
    Teal = "Teal"


class BrowStyle(Enum):
    Sparse = "Sparse"
    Standard = "Standard"
    Fluffy = "Fluffy"
    Apart = "Apart"
    Stern = "Stern"
    ThinArched = "ThinArched"
    ThickArched = "ThickArched"
    ThinFlat = "ThinFlat"
    Sliced = "Sliced"
    Simple = "Simple"
    Connected = "Connected"


class HairStyle(Enum):
    Faded_Afro = "Faded_Afro"
    Messy_Updo = "Messy_Updo"
    Receding_Wizard = "Receding_Wizard"
    Mullet = "Mullet"
    Short_Ponytail_HairMesh = "Short_Ponytail_HairMesh"
    Finger_Waves = "Finger_Waves"
    Cornrows_HairMesh = "Cornrows_HairMesh"
    Straight_Bob = "Straight_Bob"
    Whitney_Curls = "Whitney_Curls"
    Cropped_Bang = "Cropped_Bang"
    Bob = "Bob"
    Hairspray_Bob = "Hairspray_Bob"
    OldGuy_Business = "OldGuy_Business"
    Viking_Braids = "Viking_Braids"
    Dreadlocks_HairMesh = "Dreadlocks_HairMesh"
    Even_Buzz_Back = "Even_Buzz_Back"
    Ponytail_HairMesh = "Ponytail_HairMesh"
    Hollywood_curls = "Hollywood_curls"
    Messy_Business = "Messy_Business"
    Unkempt = "Unkempt"
    Top_Bun = "Top_Bun"
    Cropped = "Cropped"
    Colly_Mohawk = "Colly_Mohawk"
    Natural_Fade = "Natural_Fade"
    Short_Afro = "Short_Afro"
    Shaggy = "Shaggy"
    Flat_Top = "Flat_Top"
    Messy_Bob = "Messy_Bob"
    Spiked = "Spiked"
    Business = "Business"
    Undercut = "Undercut"
    Mullet_Mohawk = "Mullet_Mohawk"
    Buzz_Mohawk = "Buzz_Mohawk"
    None_Style = "None"
    High_and_Tight = "High_and_Tight"
    Wavy_Business = "Wavy_Business"
    CyberFade = "CyberFade"
    Tousled_Bob = "Tousled_Bob"
    Choppy_Bob = "Choppy_Bob"
    Short_Loc = "Short_Loc"


class EyelashStyle(Enum):
    Style1 = "01"
    Style2 = "02"


class HeadShapeSliders(Enum):
    square = 24
    round = 25
    narrow = 26
    wide = 27


class NeckSliders(Enum):
    wattle_in_out = 30
    narrow_wide = 31


class ChinSliders(Enum):
    narrow_wide = 34
    back_forward = 35
    down_up = 36


class JawSliders(Enum):
    narrow_wide = 38
    back_forward = 39
    down_up = 40


class CheeksSliders(Enum):
    down_up = 47
    scale_down_up = 48
    narrow_wide = 49


class MouthSliders(Enum):
    underbite_overbite = 42
    scale_down_up = 43
    left_right = 44
    down_up = 45


class NoseSliders(Enum):
    nose_tip_down_up = 51
    short_long = 52
    narrow_wide = 53
    back_forward = 54
    down_up = 55
    nostril_up_down = 75
    nostrills_in_out = 77
    rigde_narrow_wide = 78
    ridge_in_out = 79


class EarsSliders(Enum):
    narrow_wide = 57
    back_forward = 58
    down_up = 59


class EyebrowsSliders(Enum):
    narrow_wide = 61
    back_forward = 62
    down_up = 63


class EyesSliders(Enum):
    narrow_wide = 65
    scale_down_up = 67
    back_forward = 69
    down_up = 70


class ForeheadSliders(Enum):
    narrow_wide = 72
    back_forward = 73
