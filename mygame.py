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
scn.load_template(Size.TINY)

#Team
class Team:
    def __init__(self, name):
        self.name = name

        self.x1_win = None
        self.x2_win = None
        self.y1_win = None
        self.y2_win = None
        self.players = None
        self.other_team = None
        self.players_starts = [None] * 4

class Player:

    def __init__(self, id):
        self.id = id
        self.position = (None, None)
        
team1 = Team("TEAM 1")
team1.players = [Player(i) for i in range(1, 5)]

#Diplomacy
diplomacy = Trigger("Set Diplomacy", enable=1).then_(
    SendInstruction(message="Setting Diplomacy 1234",
                    color=Color.ORANGE,
                    panel_location=1, time=5))

for team in [team1]:
    for player in team.players:
        for target_player in team.players:
            diplomacy.then_(ChangeDiplomacy(source_player=player.id, target_player=target_player.id, diplomacy=0))

scn.add(diplomacy)

#Merchant
merchants = []
for team in [team1]:
    for player in team.players:
        merchant = scn.units.new(owner=player.id, x=5, y=5, unit_cons=UnitConstant.MERCHANT.value)
        merchant.reset_position = (5, 5)
        merchants.append(merchant)

#Fire
for i in range(1, 450):
    randx = random.randint(3, scn.get_width() / 3 - 1)
    randy = random.randint(3, scn.get_height() / 3 - 1)
    smoke = scn.units.new(owner=PlayerEnum.GAIA.value, x=randx+2, y=randy-1, unit_cons=UnitConstant.SMOKE.value)
    for team in [team1]:
        for player in team.players:
            fire = Trigger("Fire touching {}".format(player.id), enable=1, loop=True)
            fire \
            .if_(ObjectInArea(amount=1, source_player=player.id, unit_cons=UnitConstant.MERCHANT.value, x1=randx, x2=randx, y1=randy, y2=randy)) \
            .then_(RemoveObjectByConstant(player=player.id, unit_cons=UnitConstant.MERCHANT.value, x1=randx, x2=randx, y1=randy, y2=randy)) \
            .then_(CreateObject(player=player.id, unit_cons=UnitConstant.MERCHANT.value, x=3, y=3))
            scn.add(fire)


#Script
OFFSET_TUTO = 5
for team in [team1]:
    for player in team.players:
        offset = 0
        m1 = InstructionParameters("Welcome to Age of Total War", None, 2 * OFFSET_TUTO, Color.BLUE)
        m2 = InstructionParameters("To win a round, you need to bring 3 relics cart to this area", None, 2 * OFFSET_TUTO, Color.BLUE)
        m3 = InstructionParameters("test", None, 2 * OFFSET_TUTO, Color.BLUE)
        m4 = InstructionParameters("no", None, 2 * OFFSET_TUTO, Color.BLUE)
        messages = [m1, m2, m3, m4]
        display_tutorial = DisplayInstructions(messages=messages, name="()".format(player.id), enable=True, player=player.id, panel_location=2)
        scn.add(display_tutorial)
        
scn.save(C.game_path_scenario, "mygame")
