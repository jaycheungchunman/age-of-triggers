from aot.meta_triggers.DisplayInstructions import DisplayInstructions, InstructionParameters
from aot.meta_triggers.invicible_unit import InvicibleUnit
from aot.meta_triggers.no_house_needed import NoHouseNeeded
from aot.model.condition import *
from aot.model.effect import *
from aot.model.unit import Unit
from aot.model.enums.player import PlayerEnum
from aot.model.enums.sizes import Size
from aot.model.enums.tile import EnumTile
from aot.model.enums.unit import UnitConstant, UnitType
from aot.model.scenario import Scenario
from aot.model.trigger import Trigger
from aot.utilities.configuration import Configuration
import logging
import numpy as np
import random

logging.basicConfig(level=logging.INFO)
C = Configuration("examples/configuration_de.json")

scn = Scenario(size=Size.TINY)
scn.load(path="templates", basename="template_tiny", path_header="C:/Users/cheung/Documents/age-of-triggers/templates/header/text.txt", path_decompressed_data="C:/Users/cheung/Documents/age-of-triggers/templates/decompressed_data/text.txt")
