from aot import Scenario, Size, UnitConstant, Trigger, Timer, PlayerEnum, RemoveObject, SendInstruction, EnumTile, \
    MoveObjectToPoint, CaptureUnit, GiveExtraPop, GiveHeadroom, CreateObject, ActivateTrigger, UnitInArea, ObjectInArea, \
    Not, DesactivateTrigger, ChangeUnitOwnership, UnitType, RemoveObjectByType, PayGold, GiveGold, PayStone, GiveStone, \
    PayWood, GiveWood, PayFood, GiveFood, Color, SendChat, MoveCamera, BuffHP
from aot.metatriggers.api import NoHouseNeeded, InvicibleUnit
from aot.utilities.configuration import Configuration

C = Configuration("aot/api/configuration_de.json")

scn = Scenario(size=Size.LARGE)
#scn.load(C.game_path_scenario+"/template.aoe2scenario")
TIME_TO_TRAIN_UNITS = 200
MAX_TIME_OF_A_ROUND = 600

# TIME_TO_TRAIN_UNITS = 10
# MAX_TIME_OF_A_ROUND = 50

WIN_AREA_POSITION_RELATIVE_TO_SPAWN = 15
POPULATION = 515
SPAWN_LENGTH = 25
GOLD = 7500
FOOD = 20000
STONE = 0
WOOD = 20000
NUMBER_OF_WARNING = 10


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
team2 = Team("TEAM 2")
team2.players = [Player(i) for i in range(5, 9)]
team1.other_team = team2
team2.other_team = team1
for player in range(1, 9):
    metatrigger = NoHouseNeeded(player=player, population=POPULATION)
    scn.add(metatrigger)

for x in list(range(0, int(SPAWN_LENGTH))) + list(range(scn.get_width() - int(SPAWN_LENGTH), scn.get_width())):
    for y in range(0, scn.get_height() - 1):
        scn.map.tiles[y][x].type = EnumTile.LEAVES.value
        scn.map.tiles[y][x].elevation = 1

for team in [team1,team2]:
    for player in team.players:
        # player.disabledtechs[]
        for ennemy in team.other_team.players:
            scn.players[player.id].diplomacy.stances[ennemy.id] =3

        for ally in team.players:
            scn.players[player.id].diplomacy.stances[ally.id] =0

relics = []
for r in range(1, 4):
    x = int(scn.get_width() / 2)
    y = int(r * (scn.get_height() / 4))
    relic = scn.units.new(owner=0, x=x, y=y, type=UnitConstant.RELIC_CART.value)
    relic.reset_position = (x, y)
    relics.append(relic)
    for player in range(1, 9):
        scn.units.new(owner=player, x=x, y=y, type=UnitConstant.MAP_REVEAL.value)


def create_win_area(x, y, sep=4, team=None):
    for unit_constant in [UnitConstant.FLAG_A.value, UnitConstant.ARMY_TENT_4.value]:
        uns = [scn.units.new(owner=team.players[0].id, x=x, y=y, type=unit_constant),
               scn.units.new(owner=team.players[1].id, x=x + sep, y=y + sep, type=unit_constant),
               scn.units.new(owner=team.players[2].id, x=x, y=y + sep, type=unit_constant),
               scn.units.new(owner=team.players[3].id, x=x + sep, y=y, type=unit_constant)]
        if unit_constant == UnitConstant.ARMY_TENT_4.value:
            for iu, u in enumerate(uns):
                mt = Trigger("buff unit ({})".format(u.id),enable=True).then_(BuffHP(unit=u,amount=90000,player=team.players[iu].id))
                # mt = InvicibleUnit(unithp=550, unit=u, player=team.players[iu].id)
                scn.add(mt)

    for tile in scn.map.tiles.getArea(x, y, x + sep - 1, y + sep - 1):
        tile.type = EnumTile.ROCK.value
    for player in range(1, 9):
        scn.units.new(owner=player, x=x + int(sep / 2), y=y + int(sep / 2), type=UnitConstant.MAP_REVEAL.value)

    for ir, relic in enumerate(relics):
        create_flag_score = Trigger("create_flag_score", enable=True)
        remove_flag_score = Trigger("remove_flag_score")

        create_flag_score.if_(UnitInArea(player=0, unit=relic, x1=x, x2=x + sep - 1, y1=y, y2=y + sep - 1))
        create_flag_score.then_(
            CreateObject(player=0, x=x + int(sep / 2), y=y + int(sep / 2) - 1 + ir,
                         unit_cons=UnitConstant.FLAG_B.value))
        create_flag_score.then_(ActivateTrigger(remove_flag_score))
        scn.add(create_flag_score)

        remove_flag_score.if_(Not(UnitInArea(player=0, unit=relic, x1=x, x2=x + sep - 1, y1=y, y2=y + sep - 1)))
        remove_flag_score.then_(
            RemoveObject(player=0,
                         x1=x + int(sep / 2), y1=y + int(sep / 2) - 1 + ir,
                         x2=x + int(sep / 2), y2=y + int(sep / 2) - 1 + ir,
                         unit_cons=UnitConstant.FLAG_B.value))
        remove_flag_score.then_(ActivateTrigger(create_flag_score))
        scn.add(remove_flag_score)

    team.x1_win = x
    team.y1_win = y
    team.x2_win = x + sep
    team.y2_win = y + sep


position_win_area = WIN_AREA_POSITION_RELATIVE_TO_SPAWN + int(SPAWN_LENGTH)
sep_win_area = 5
create_win_area(x=position_win_area,
                y=int(scn.get_height() / 2 - sep_win_area / 2),
                sep=sep_win_area,
                team=team1)
create_win_area(x=scn.get_width() - position_win_area - sep_win_area,
                y=int(scn.get_height() / 2 - sep_win_area / 2),
                sep=sep_win_area,
                team=team2)

for team in [team1, team2]:
    for p in team.players:
        x, y = team.x1_win + int(sep_win_area / 2), team.y1_win + int(sep_win_area / 2)
        for ir, relic in enumerate(relics):
            t = Trigger("move relics({}) P{}".format(relic.id, p.id), enable=True, loop=True)
            t.if_(CaptureUnit(player=p.id, unit=relic))
            t.then_(MoveObjectToPoint(player=p.id, unit=relic, x=x, y=y - 1 + ir))
            scn.add(t)

relic_reset_triggers = []

for ir, relic in enumerate(relics):
    t = Trigger("move back relics({}) ".format(relic.id))
    t.then_(ChangeUnitOwnership(sourcePlayer=0, targetPlayer=0, unit=relic))
    t.then_(MoveObjectToPoint(player=0, unit=relic, x=relic.reset_position[0], y=relic.reset_position[1]))
    scn.add(t)
    relic_reset_triggers.append(t)

buildings = [UnitConstant.CASTLE.value,
             UnitConstant.ARCHERY_RANGE.value,
             UnitConstant.MONASTERY.value,
             UnitConstant.BARRACKS.value,
             UnitConstant.SIEGE_WORKSHOP.value,
             UnitConstant.STABLE.value

             ]

SEP_BETWEEN_BUILDING = 4
OFFSET = int(((len(buildings) - 1) * SEP_BETWEEN_BUILDING) / 2)

create_buildings = Trigger("create buildings")
remove_buildings = Trigger("remove buildings")
for team in [team1, team2]:
    for player in team.players:
        if player.id > 4:
            x = scn.get_width() - 4
        else:
            x = 4
        y = int(((player.id % 4) + 1) * (scn.get_height() / 5))
        player.position = (x, y)
        # scn.units.new(owner=player, x=x + (2 if player < 5 else -2), y=y, type=UnitConstant.FLAG_B.value)
        for i_unit, unit in enumerate(buildings):
            y_ = y + i_unit * SEP_BETWEEN_BUILDING - OFFSET
            create_buildings.then_(CreateObject(x=x, y=y_, unit_cons=unit, player=player.id))
            remove_buildings.then_(RemoveObject(player=player.id, unit_cons=unit, x1=x, x2=x, y1=y_, y2=y_))
scn.add(create_buildings)
scn.add(remove_buildings)

remove_haystacks = Trigger("open fighting area")
remove_haystacks.then_((RemoveObject(player=PlayerEnum.GAIA.value,
                                     unit_cons=UnitConstant.HAY_STACK.value,
                                     x1=int(SPAWN_LENGTH),
                                     x2=int(SPAWN_LENGTH),
                                     y1=0,
                                     y2=scn.get_width() - 1)))
remove_haystacks.then_((RemoveObject(player=PlayerEnum.GAIA.value,
                                     unit_cons=UnitConstant.HAY_STACK.value,
                                     x1=scn.get_width() - (int(SPAWN_LENGTH) + 1),
                                     x2=scn.get_width() - (int(SPAWN_LENGTH) + 1),
                                     y1=0,
                                     y2=scn.get_height() - 1)))
remove_haystacks.then_(SendInstruction(text="You may now fight"))
scn.add(remove_haystacks)

create_haystacks = Trigger("create haystacks")
for x in [SPAWN_LENGTH, scn.get_width() - SPAWN_LENGTH - 1]:
    for y in range(0, scn.get_height()):
        create_haystacks.then_(CreateObject(x=x, y=y, unit_cons=UnitConstant.HAY_STACK.value, player=0))
scn.add(create_haystacks)

kill_all_military = Trigger("kill all military")
for p in range(1, 9):
    kill_all_military.then_(RemoveObjectByType(player=p, x1=-1, x2=-1, y2=-1, y1=-1, type=UnitType.MILITARY.value))
scn.add(kill_all_military)

set_resource = Trigger("Resources")
for p in range(1, 9):
    set_resource.then_(PayGold(player=p, amount=GOLD))
    set_resource.then_(PayFood(player=p, amount=FOOD))
    set_resource.then_(PayStone(player=p, amount=10000 if STONE == 0 else STONE))
    set_resource.then_(PayWood(player=p, amount=WOOD))
    set_resource.then_(GiveGold(player=p, amount=GOLD))
    set_resource.then_(GiveStone(player=p, amount=STONE))
    set_resource.then_(GiveWood(player=p, amount=WOOD))
    set_resource.then_(GiveFood(player=p, amount=FOOD))

reset_resource = Trigger("reset Resources")
for p in range(1, 9):
    reset_resource.then_(PayGold(player=p, amount=GOLD))
    reset_resource.then_(PayFood(player=p, amount=FOOD))
    reset_resource.then_(PayStone(player=p, amount=10000 if STONE == 0 else STONE))
    reset_resource.then_(PayWood(player=p, amount=WOOD))

scn.add(set_resource)
scn.add(reset_resource)

new_round = Trigger("new_round", enable=True)

for t in relic_reset_triggers:
    new_round.then_(ActivateTrigger(t))

for team in [team1, team2]:
    for p in team.players:
        new_round.then_(
            SendChat(player=p.id, color=Color.RED,
                     text="<<< TRAIN YOUR UNITS ! YOU HAVE {}s >>>".format(TIME_TO_TRAIN_UNITS)))
        new_round.then_(MoveCamera(player=p.id, x=p.position[0], y=p.position[1]))
new_round.then_(ActivateTrigger(set_resource))
new_round.then_(ActivateTrigger(create_buildings))
new_round.then_(ActivateTrigger(create_haystacks))
new_round.then_(ActivateTrigger(kill_all_military))

open_area = Trigger("Open Area")
open_area.then_(ActivateTrigger(reset_resource))
open_area.if_(Timer(TIME_TO_TRAIN_UNITS))
open_area.then_(ActivateTrigger(remove_haystacks))
open_area.then_(ActivateTrigger(remove_buildings))

new_round.then_(ActivateTrigger(open_area))

for team in [team1, team2]:
    remove_flag = Trigger("remove flags ({})".format(team.name))
    remove_flag.then_(
        RemoveObject(player=0, unit_cons=UnitConstant.FLAG_B.value,
                     x1=team.x1_win, x2=team.x2_win, y1=team.y1_win, y2=team.y2_win))
    remove_flag.then_(SendInstruction(text=team.name + " lost a relic, countdown reset to zero", color=Color.RED))

    countdowns_triggers = []
    for i in range(0, NUMBER_OF_WARNING):
        time_ = i * int(MAX_TIME_OF_A_ROUND / NUMBER_OF_WARNING)
        t = Trigger("countdown {}s ({})".format(time_, team.name))
        t.if_(Timer(time_))
        t.then_(
            SendInstruction(color=Color.RED, text=team.name + " will win in {}s".format(MAX_TIME_OF_A_ROUND - time_)))
        scn.add(t)
        countdowns_triggers.append(t)

    compute_win = Trigger("compute_win ({})".format(team.name))
    compute_win_no_military = Trigger("compute_win_no_military ({})".format(team.name))
    compute_instant_win = Trigger("compute_instant_win ({})".format(team.name))


    # win is less than 5 militry for each player TODO factorise wining conditions
    compute_win_no_military.if_(Timer(int(MAX_TIME_OF_A_ROUND/10))) # REMIOVE THIS, BUT THIS WILL BUG AND AUTOWIN ??
    for p in team.other_team.players:
        compute_win_no_military.if_(
            Not(ObjectInArea(amount=5, sourcePlayer=p.id, unit_type=UnitType.MILITARY.value, x1=-1, x2=-1, y1=-1,
                             y2=-1)))
    for p in team.players:
        compute_win_no_military.if_(
            (ObjectInArea(amount=5, sourcePlayer=p.id, unit_type=UnitType.MILITARY.value, x1=-1, x2=-1, y1=-1,
                             y2=-1)))
    compute_win_no_military.then_(ActivateTrigger(remove_flag))
    for p in range(1,9):
        compute_win_no_military.then_(
            SendChat(player=p,text="<<<<<<<<< {} wins this round >>>>>>>>>>".format(team.name), color=Color.RED))
    compute_win_no_military.then_(DesactivateTrigger(compute_win))
    for t in countdowns_triggers:
        compute_win_no_military.then_(DesactivateTrigger(t))
    compute_win_no_military.then_(ActivateTrigger(new_round))

    # win after 10 win for anyone with 2 relics
    have_X_relic = lambda amount: ObjectInArea(sourcePlayer=0, unit_cons=UnitConstant.FLAG_B.value, amount=amount,
                                               x1=team.x1_win + int((team.x2_win - team.x1_win) / 2),
                                               x2=team.x1_win + int((team.x2_win - team.x1_win) / 2),
                                               y1=team.y1_win + int((team.y2_win - team.y1_win) / 2) - 1,
                                               y2=team.y1_win + int((team.y2_win - team.y1_win) / 2) + 1)
    show_countdown = Trigger("show countdown {}".format(team.name))
    show_countdown.if_(have_X_relic(2))
    # show_countdown.if_(Not(have_X_relic(3)))
    for t in countdowns_triggers:
        show_countdown.then_(ActivateTrigger(t))

    compute_win.if_(have_X_relic(2))
    compute_win.if_(Timer(MAX_TIME_OF_A_ROUND))
    compute_win.then_(ActivateTrigger(remove_flag))
    for p in range(1, 9):
        compute_win.then_(
            SendChat(player=p, text="<<<<<<<<< {} wins this round >>>>>>>>>>".format(team.name), color=Color.RED))

    compute_win.then_(ActivateTrigger(new_round))

    # instant win if 3 relics
    compute_instant_win.if_(ObjectInArea(sourcePlayer=0, unit_cons=UnitConstant.FLAG_B.value, amount=3,
                                         x1=team.x1_win + int((team.x2_win - team.x1_win) / 2),
                                         x2=team.x1_win + int((team.x2_win - team.x1_win) / 2),
                                         y1=team.y1_win + int((team.y2_win - team.y1_win) / 2) - 1,
                                         y2=team.y1_win + int((team.y2_win - team.y1_win) / 2) + 1))

    compute_instant_win.then_(ActivateTrigger(remove_flag))
    for p in range(1, 9):
        compute_instant_win.then_(
            SendChat(player=p, text="<<<<<<<<< {} wins this round >>>>>>>>>>".format(team.name), color=Color.RED))
    compute_instant_win.then_(DesactivateTrigger(compute_win))
    for t in countdowns_triggers:
        compute_instant_win.then_(DesactivateTrigger(t))
    compute_instant_win.then_(ActivateTrigger(new_round))

    open_area.then_(ActivateTrigger(compute_win))
    open_area.then_(ActivateTrigger(show_countdown))
    open_area.then_(ActivateTrigger(compute_instant_win))
    open_area.then_(ActivateTrigger(compute_win_no_military))

    remove_flag.then_(DesactivateTrigger(compute_win))
    for t in countdowns_triggers:
        remove_flag.then_(DesactivateTrigger(t))

    scn.add(remove_flag)
    scn.add(compute_win)
    scn.add(compute_instant_win)
    scn.add(compute_win_no_military)
    scn.add(show_countdown)

scn.add(new_round)
scn.add(open_area)
scn.save(C.game_path_scenario, "age-of-total-war")

# TODO make tent invincible
# TODO make auto win if no military or less than 5on fighting area
# scn.save("Z:/steam/steamapps/common/Age2HD/mods/age of total war/resources/_common/examples",
#          "age-of-total-war 0.2 [template]")
