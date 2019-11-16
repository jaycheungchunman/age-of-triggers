from enum import Enum


class EffectType(Enum):

    ACTIVATE_TRIGGER = 8
    # TODO add all from eEffect

eEffect = {
    0: "Invalid Effect",
    1: "Change Diplomacy",
    2: "Research Technology",
    3: "Send Chat",
    4: "Play Sound",
    5: "Send Tribute",
    6: "Unlock Gate",
    7: "Lock Gate",
    8: "Activate Trigger",
    9: "Deactivate Trigger",
    10: "AI Script Goal",
    11: "Create Object",
    12: "Task Object",
    13: "Declare Victory",
    14: "Kill Object",
    15: "Remove Object",
    16: "Change View",
    17: "Unload",
    18: "Change Ownership",
    19: "Patrol",
    20: "Display Instructions",
    21: "Clear Instructions",
    22: "Freeze Unit",
    23: "Use Advanced Buttons",
    24: "Damage Object",
    25: "Place Foundation",
    26: "Change Object Name",
    27: "Change Object HP",
    28: "Change Object Attack",
    29: "Stop Unit",
    30: "Snap View",
    31: "Unknown",
    32: "Enable Tech",
    33: "Disable Tech",
    34: "Enable Unit",
    35: "Disable Unit",
    36: "Flash Objects"
}