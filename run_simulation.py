
from classes.TargetShip import TargetShip
from classes.OwnShip import OwnShip
from classes.State import State, read_state
from modules.collision_parameter_module import calculate_state_collision_parameters, print_collision_parameters
from modules.encounter_situation_module import calculate_state_encounter_situations


state = State()

os = OwnShip(0, 0, 90, 5, 100)
ts1 = TargetShip(3.5, 3.5, 180, 4, 60)
ts2 = TargetShip(5, -8, 10, 8, 120)
ts3 = TargetShip(-5, -1, 95, 12, 150)
ts4 = TargetShip(-2, 5.7, 280, 2, 250)
ts5 = TargetShip(9, 0.5, 270, 5, 80)

state.add_own_ship(os)
state.add_target_ship(ts1)
state.add_target_ship(ts2)
state.add_target_ship(ts3)
state.add_target_ship(ts4)
state.add_target_ship(ts5)

path = "state/state.json"
state.write_state(path)

# state = read_state(path)

timesteps = 2
scale = 10
timefactor = 6

for i in range(timesteps):
    coll_parameters = calculate_state_collision_parameters(state.get_state())
    enc_situations = calculate_state_encounter_situations(coll_parameters)
    state.plot(scale, coll_parameters, enc_situations)
    print("Timestep: " + str(i + 1))
    print_collision_parameters(coll_parameters)
    state = state.next_state(timefactor)
