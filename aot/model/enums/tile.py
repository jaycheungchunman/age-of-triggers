from enum import Enum


class EnumTile(Enum):
    ROCK=40
    LEAVES=5
    BLACK_GRASS=41
    PALM_DESERT=13
    ICE=26
    FOREST=10
    WATER_SHALLOW=1
    SNOW=33
    GRASS=0
    ROAD=24
    SHALLOWS=4
    ROCK_ROAD=40
    ICE_ALLOW_SHIP=35
    BEACH=2
    NOBUILDING=2

# TODO
eTile = {
    0: "Grass 1 (default terrain)",
    1: "Water, Shallow",
    2: "Beach (no buildings)",
    3: "Dirt 3 (grassy)",
    4: "Shallows",
    5: "Leaves",
    6: "Dirt 1 (brown with occasional cactus)",
    7: "Farm",
    8: "Dead Farm",
    9: "Grass 3 (brownish)",
    10: "Forest",
    11: "Dirt 2 (dirt grass mixture)",
    12: "Grass 2 (lush / very green)",
    13: "Palm Desert",
    14: "Desert (sandy and light colored)",
    15: "Water (not dockable)",
    16: "Looks like Grass 1 (can build, only siege can move)",
    17: "Jungle",
    18: "Bamboo",
    19: "Pine Forest",
    20: "Forest (says oak forest when clicking tree)",
    21: "Snow Pine Forest",
    22: "Water, Deep",
    23: "Water, Medium",
    24: "Road",
    25: "Road, Broken",
    26: "Ice (no ships)",
    27: "Dirt 2 (no beach, building residue, dockable)",
    28: "Water, Bridge (walkable, no ships)",
    29: "Farm 1",
    30: "Farm 2",
    31: "Farm 3",
    32: "Snow",
    33: "Snow Dirt",
    34: "Snow Grass",
    35: "Ice (allows ships)",
    36: "Snow Dirt (building residue)",
    37: "Ice, Beach (allows ships, build walls only)",
    38: "Road, Snow",
    39: "Road, Fungus",
    40: "Rock / Road (no buildings)",
    41: "Looks like grass 1 (nobuild, crazy pathfinding, black on map)"
}

# TODO
eTileColor = {
    0: (51, 153, 39),
    1: (48, 93, 182),
    2: (232, 180, 120),
    3: (228, 162, 82),
    4: (84, 146, 176),
    5: (51, 153, 39),
    6: (228, 162, 82),
    7: (130, 136, 77),
    8: (130, 136, 77),
    9: (51, 153, 39),
    10: (21, 118, 21),
    11: (228, 162, 82),
    12: (51, 153, 39),
    13: (21, 118, 21),
    14: (232, 180, 120),
    15: (48, 93, 182),
    16: (51, 153, 39),
    17: (21, 118, 21),
    18: (21, 118, 21),
    19: (21, 118, 21),
    20: (21, 118, 21),
    21: (21, 118, 21),
    22: (0, 74, 187),
    23: (0, 74, 187),
    24: (228, 162, 82),
    25: (228, 162, 82),
    26: (255, 236, 73),
    27: (228, 162, 82),
    28: (48, 93, 182),
    29: (130, 136, 77),
    30: (130, 136, 77),
    31: (130, 136, 77),
    32: (200, 216, 255),
    33: (200, 216, 255),
    34: (200, 216, 255),
    35: (152, 192, 240),
    36: (200, 216, 255),
    37: (152, 192, 240),
    38: (200, 216, 255),
    39: (200, 216, 255),
    40: (228, 162, 82),
    41: (0, 0, 0)
}
