# from teams.helper_function import Troops, Utils

# team_name = "MUMBAI"
# troops = [Troops.prince,Troops.minion,Troops.archer,Troops.giant,Troops.dragon,Troops.skeleton,Troops.balloon,Troops.barbarian]
# deploy_list = Troops([])
# team_signal = "h"

# def deploy(arena_data:dict):
#     """
#     DON'T TEMPER DEPLOY FUCNTION
#     """
#     deploy_list.list_ = []
#     logic(arena_data)
#     return deploy_list.list_, team_signal

# def logic(arena_data:dict):
#     global team_signal
#     deploy_list.deploy_prince((-16,0))
#     """
#     WRITE YOUR CODE HERE 
#     """

import random
from teams.helper_function import Troops, Utils

team_name = "YOYO"
troops = [
    Troops.wizard, Troops.minion, Troops.archer, Troops.prince,
    Troops.dragon, Troops.knight, Troops.valkyrie, Troops.skeleton
]

deploy_list = Troops([])
team_signal = ""

def random_x(min_val=-25, max_val=25):
    return random.randint(min_val, max_val)

def deploy(arena_data: dict):
    """
    DON'T TEMPER DEPLOY FUNCTION
    """
    deploy_list.list_ = []
    logic(arena_data)
    return deploy_list.list_, team_signal

def logic(arena_data: dict):
    global team_signal
    my_tower = arena_data["MyTower"]
    opp_troops = arena_data["OppTroops"]
    
    # --- Update Team Signal ---
    # Add new opponent troop names (avoid duplicates).
    for troop in opp_troops:
        current_names = [name.strip() for name in team_signal.split(",")] if team_signal else []
        if troop.name not in current_names:
            team_signal = team_signal + ", " + troop.name if team_signal else troop.name
    print(f"Team Signal: {team_signal}")
    
    # --- Analyze Opponent's Deck Composition ---
    # Define opponent categories.
    opponent_air = {"Minion", "Dragon", "Musketeer"}
    opponent_ground = {"Prince", "Knight", "Barbarian", "Princess"}
    
    tokens = [token.strip() for token in team_signal.split(",") if token.strip() != "h"]
    count_air = sum(1 for token in tokens if token in opponent_air)
    count_ground = sum(1 for token in tokens if token in opponent_ground)
    troops_all={"Archer", "Minion", "Knight", "Skeleton", "Dragon", "Valkyrie","Musketeer", "Giant", "Prince", "Barbarian", "Balloon", "Wizard"}
    points ={{0 for i in range (8)} for j in range (0,12)}
    points[0] = {9, 9, 9, 8, 7, 8, 7, 6, 6, 9, 7, 5}# wizard
    points[1] = {5, 5, 9, 8, 6, 3, 5, 6, 6, 7, 6, 1} # minions
    points[2] = {5, 6, 4, 3, 5, 3, 6, 6, 3, 7, 8, 2} #archer
    points[3] = {8, 4, 6, 1, 2, 7, 8, 8, 5, 7, 0, 5} #prince
    points[4] = {5, 7, 8, 9, 5, 7, 4, 7, 7, 8, 8, 2} # dragon
    points[5] = {7, 3, 5, 1, 3, 6, 7, 7, 4, 6, 0 , 5} #knight
    for i in range (0,12):
        for j in range (0,12):
            if i==j:                
                points[i][j]=5
    points[0] = {}
    if count_ground > count_air:
        recommended_counter = "air"    # Counter ground with air units.
    elif count_air > count_ground:
        recommended_counter = "ground" # Counter air with ground units.
    else:
        recommended_counter = None     # No clear preference.
    
    # --- Score Our Troops (only from deployable troops) ---
    deployable = my_tower.deployable_troops
    # Define base scores and categories for our troops.
    troop_data = {
        Troops.wizard:    {"score": 6, "category": "air",    "name": "Wizard"},
        Troops.minion:    {"score": 4, "category": "air",    "name": "Minion"},
        Troops.archer:    {"score": 2, "category": "air", "name": "Archer"},
        Troops.musketeer:     {"score": 4, "category": "air", "name": "Musketeer"},
        Troops.dragon:    {"score": 5, "category": "air",    "name": "Dragon"},
        Troops.skeleton:  {"score": 3, "category": "ground", "name": "Skeleton"},
        Troops.valkyrie:   {"score": 4, "category": "air",    "name": "Valkyrie"},
        Troops.barbarian: {"score": 3, "category": "ground", "name": "Barbarian"}
    }
    
    bonus = 3  # Bonus for matching the recommended counter strategy.
    best_troop = None
    best_score = -1
    
    # Loop over our full troop list, but only consider those that are deployable.
    for troop in troops:
        if troop not in deployable:
            continue
        base = troop_data[troop]["score"]
        cat = troop_data[troop]["category"]
        score = base + (bonus if recommended_counter and cat == recommended_counter else 0)
        if score > best_score:
            best_score = score
            best_troop = troop
    # --- Deployment Position ---
    p=0
    n=0
    y_min = 100
    for troop in arena_data["OppTroops"]:
        y_min = y_min if y_min<troop.position[1] else troop.position[1]
        if(troop.position[0]>0):
            p+=1 if troop.name != "Skeleton" else 0.2
        else:
            n+=1 if troop.name != "Skeleton" else 0.2
    if best_troop is not None:
        selected_category = troop_data[best_troop]["category"]
        if(y_min<20):
            y_pos = 0
        elif(y_min>70):
            y_pos = 50
        else:
            y_pos = y_min -20
        if selected_category == "air":
            # Deploy air units further forward.
            if p>n :
                deploy_position = (random_x(5, 20), y_pos)
            elif n>p:
                deploy_position = (random_x(-20, -5),  y_pos)
            else:
                deploy_position = (0, 0)
        else:
            # Deploy ground units slightly closer for support.
            deploy_position = (random_x(-10, 10), 0)
        deploy_list.list_.append((best_troop, deploy_position))
    else:
        # Fallback: If no deployable troop meets criteria, deploy the first available troop.
        if deployable:
            deploy_list.list_.append((deployable[0], (0, 0)))
