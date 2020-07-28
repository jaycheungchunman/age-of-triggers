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

test = Trigger("Build Wonder Time (need change)", enable=1, loop=False)
test.then_(ModifyAttribute(source_player=1))
test.then_(ModifyAttribute(source_player=2))
test.then_(ModifyAttribute(source_player=3))
test.then_(ModifyAttribute(source_player=4))
test.then_(ModifyAttribute(source_player=5))
test.then_(ModifyAttribute(source_player=6))
test.then_(ModifyAttribute(source_player=7))
test.then_(ModifyAttribute(source_player=8))
test.then_(ModifyAttributeCastle(source_player=1))
test.then_(ModifyAttributeCastle(source_player=2))
test.then_(ModifyAttributeCastle(source_player=3))
test.then_(ModifyAttributeCastle(source_player=4))
test.then_(ModifyAttributeCastle(source_player=5))
test.then_(ModifyAttributeCastle(source_player=6))
test.then_(ModifyAttributeCastle(source_player=7))
test.then_(ModifyAttributeCastle(source_player=8))
scn.add(test)

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
        self.players_starts = [None] * 8

class Player:

    def __init__(self, id):
        self.id = id
        self.position = (None, None)
        
team1 = Team("TEAM 1")
team1.players = [Player(i) for i in range(1, 9)]

#Size
width = scn.get_width()
height = scn.get_height()

for x in range(0, width):
    for y in range(0, height):
        scn.map.tiles[x][y].type = EnumTile.NOBUILDING.value
        
#Diplomacy
diplomacy = Trigger("Set Diplomacy", enable=1).then_(
    SendInstruction(message="Welcome to The War of Trebuchet.",
                    color=Color.ORANGE,
                    panel_location=0, time=30)).then_(
    SendInstruction(message="Build a Wonder to obtain Trebuchets or Cannon Galleons. Build a Castle to obtain Flamming Camels or Photonmen.",
                    color=Color.ORANGE,
                    panel_location=1, time=30)).then_(
    SendInstruction(message="Win by defending your Wonder by 200 years or killing all enemies",
                    color=Color.ORANGE,
                    panel_location=2, time=30))



for team in [team1]:
    for player in team.players:
        for target_player in team.players:
            diplomacy.then_(ChangeDiplomacy(source_player=player.id, target_player=target_player.id, diplomacy=3))

scn.add(diplomacy)

#Villager_Male
merchants = []
for team in [team1]:
    for player in team.players:
        merchant = scn.units.new(owner=player.id, x=round(width/2), y=round(height/2), unit_cons=UnitConstant.VILLAGER_MALE.value)
        merchant.reset_position = (5, 5)
        merchants.append(merchant)

buffTrigger = Trigger("10000HP for Villager", enable=1, loop=False)
for player in range(1, 9):
    buffTrigger.then_(SetHPByType(player=player, amount=10000, unit_type=UnitType.CIVILIAN.value))
scn.add(buffTrigger)

#Wonder
widthOfArea = 13
heightOfArea = 13
numberOfArea = 9
radius1 = 7
radius2 = 5
radius3 = 6
circleCenter = widthOfArea / 2 - 1
makeArea = True
for x in range(0, numberOfArea):
    for y in range(0, numberOfArea):
        if (makeArea):
            makeArea = False
            x1 = x * widthOfArea
            y1 = y * heightOfArea
            x2 = x * widthOfArea + widthOfArea
            y2 = y * heightOfArea + heightOfArea
            for xtile in range(x1, x2+1):
                for ytile in range(y1, y2+1):
                    xlength = x2-xtile-1
                    ylength = y2-ytile-1
                    if (x % 2 == 0): 
                        if ( round( ( (circleCenter - xlength)**2 + (circleCenter - ylength)**2 )**(1/2) ) == radius1 or round( ( (circleCenter - xlength)**2 + (circleCenter - ylength)**2 )**(1/2) ) == radius2):
                            scn.map.tiles[xtile][ytile].type = EnumTile.SHALLOWS.value
                        else:
                            scn.map.tiles[xtile][ytile].type = EnumTile.ROAD.value
                        scn.map.tiles[round((y2+y1)/2)][x2+1].type = EnumTile.ROAD.value
                    else:
                        if ( round( ( (circleCenter - xlength)**2 + (circleCenter - ylength)**2 )**(1/2) ) == radius1 or round( ( (circleCenter - xlength)**2 + (circleCenter - ylength)**2 )**(1/2) ) == radius3):
                            scn.map.tiles[xtile][ytile].type = EnumTile.SHALLOWS.value
                        else:
                            scn.map.tiles[xtile][ytile].type = EnumTile.GRASS.value
                        scn.map.tiles[round((y2+y1)/2)][x2+1].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)][x2].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)][x2-1].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)+1][x2+1].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)+1][x2].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)+1][x2-1].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)-1][x2+1].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)-1][x2].type = EnumTile.SHALLOWS.value
                        scn.map.tiles[round((y2+y1)/2)-1][x2-1].type = EnumTile.SHALLOWS.value
            for player in range(1, 9):
                if (x % 2 == 0): 
                    fire = Trigger("Wonder Exist {} x:{} y:{}".format(player, x, y), enable=1, loop=True)
                    fire \
                    .if_(ObjectInArea(amount=1, source_player=player, unit_cons=UnitConstant.WONDER.value, x1=x1, x2=x2, y1=y1, y2=y2)) \
                    .then_(CreateObject(player=player, unit_cons=UnitConstant.TREBUCHET_PACKED.value, x=x2+1, y=round((y2+y1)/2))) \
                    .then_(MoveObjectToPointByConstant(player=player, unit_cons=UnitConstant.TREBUCHET_PACKED.value, x1=x2+1, y1=round((y2+y1)/2), x2=x2+1, y2=round((y2+y1)/2), x=x2+1, y=y2))
                    scn.add(fire)
                    
                    photon = Trigger("Castle Exist {} x:{} y:{}".format(player, x, y), enable=1, loop=True)
                    photon \
                    .if_(ObjectInArea(amount=1, source_player=player, unit_cons=UnitConstant.CASTLE.value, x1=x1, x2=x2, y1=y1, y2=y2)) \
                    .then_(CreateObject(player=player, unit_cons=UnitConstant.PHOTONMAN.value, x=x2+1, y=round((y2+y1)/2))) \
                    .then_(ChangeUnitSpeed(player=player, unit_cons=UnitConstant.PHOTONMAN.value, x1=x2+1, y1=round((y2+y1)/2), x2=x2+1, y2=round((y2+y1)/2), x=x2+1, y=y2, amount=-2)) \
                    .then_(BuffHPByUnitCons(player=player, unit_cons=UnitConstant.PHOTONMAN.value, x1=x2+1, y1=round((y2+y1)/2), x2=x2+1, y2=round((y2+y1)/2), x=x2+1, y=y2, amount=-79)) \
                    .then_(MoveObjectToPointByConstant(player=player, unit_cons=UnitConstant.PHOTONMAN.value, x1=x2+1, y1=round((y2+y1)/2), x2=x2+1, y2=round((y2+y1)/2), x=x2+1, y=y2))
                    scn.add(photon)
                else:
                    water = Trigger("Wonder Exist {} x:{} y:{}".format(player, x, y), enable=1, loop=True)
                    water \
                    .if_(ObjectInArea(amount=1, source_player=player, unit_cons=UnitConstant.WONDER.value, x1=x1, x2=x2, y1=y1, y2=y2)) \
                    .then_(CreateObject(player=player, unit_cons=UnitConstant.ELITE_CANNON_GALLEON.value, x=x2, y=round((y2+y1)/2))) \
                    .then_(MoveObjectToPointByConstant(player=player, unit_cons=UnitConstant.ELITE_CANNON_GALLEON.value, x1=x2, y1=round((y2+y1)/2), x2=x2, y2=round((y2+y1)/2), x=x1+1, y=round((y2+y1)/2)))
                    scn.add(water)
                    
                    camel = Trigger("Castle Exist {} x:{} y:{}".format(player, x, y), enable=1, loop=True)
                    camel \
                    .if_(ObjectInArea(amount=1, source_player=player, unit_cons=UnitConstant.CASTLE.value, x1=x1, x2=x2, y1=y1, y2=y2)) \
                    .then_(CreateObject(player=player, unit_cons=UnitConstant.FLAMINGCAMEL.value, x=x2, y=round((y2+y1)/2))) \
                    .then_(ChangeUnitSpeed(player=player, unit_cons=UnitConstant.FLAMINGCAMEL.value, x1=x2, y1=round((y2+y1)/2), x2=x2, y2=round((y2+y1)/2), x=x2+1, y=y2, amount=20)) \
                    .then_(MoveObjectToPointByConstant(player=player, unit_cons=UnitConstant.FLAMINGCAMEL.value, x1=x2, y1=round((y2+y1)/2), x2=x2, y2=round((y2+y1)/2), x=x1+1, y=round((y2+y1)/2)))
                    scn.add(camel)
        else:
            makeArea = True

# GIVE RESSOURCES
GOLD = 10000
FOOD = 0
STONE = 10000
WOOD = 10500

set_resource = Trigger("Resources", enable=1, loop=False)
scn.add(set_resource)

for p in range(1, 9):
    set_resource.then_(PayGold(player=p, amount=GOLD))
    set_resource.then_(PayFood(player=p, amount=FOOD))
    set_resource.then_(PayStone(player=p, amount=10000 if STONE == 0 else STONE))
    set_resource.then_(PayWood(player=p, amount=WOOD))
    set_resource.then_(GiveGold(player=p, amount=GOLD))
    set_resource.then_(GiveStone(player=p, amount=STONE))
    set_resource.then_(GiveWood(player=p, amount=WOOD))
    set_resource.then_(GiveFood(player=p, amount=FOOD))

scn.save(C.game_path_scenario, "The_War_Of_Trebuchet_3_0_0")
