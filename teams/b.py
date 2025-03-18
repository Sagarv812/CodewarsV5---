# from teams.helper_function import Troops, Utils

# team_name = "DELHI"
# troops = [Troops.dragon,Troops.skeleton,Troops.wizard,Troops.minion,Troops.archer,Troops.giant,Troops.balloon,Troops.skeleton]
# deploy_list = Troops([])
# team_signal = ""

# def deploy(arena_data:dict):
#     """
#     DON'T TEMPER DEPLOY FUCNTION
#     """
#     deploy_list.list_ = []
#     logic(arena_data)
#     return deploy_list.list_, team_signal

# def logic(arena_data:dict):
#     global team_signal
#     deploy_list.deploy_dragon((-16,0))

from teams.helper_function import Troops, Utils

team_name = "Priyam"
troops = [Troops.wizard,Troops.valkyrie,Troops.archer,Troops.knight,Troops.dragon,Troops.prince,Troops.barbarian,Troops.skeleton]
deploy_list = Troops([])
team_signal = ""

def deploy(arena_data:dict):
    """
    DON'T TEMPER DEPLOY FUCNTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data:dict):
    global team_signal
    if(Troops.knight in arena_data["MyTower"].deployable_troops):
        for troop in arena_data["OppTroops"]:
            if(troop.name == "Wizard"):
                print(troop.position)
                if(troop.position[1]<-10):
                    deploy_list.list_.append((Troops.knight,(troop.position[0],60 + troop.position[1])))
    else:
        deploy_list.list_.append((arena_data["MyTower"].deployable_troops[0],(-25,0)))
