
from classes.TargetVessel import TargetVessel
from classes.OwnVessel import OwnVessel
from classes.State import State
from modules.collision_parameter_module import calculate_state_collision_parameters, print_collision_parameters
from modules.encounter_situation_module import calculate_state_encounter_situations


state = State()

ov = OwnVessel(0, 0, 90, 5, 100)
tv1 = TargetVessel(3.5, 3.5, 180, 4, 60)
tv2 = TargetVessel(5, -8, 10, 8, 120)
tv3 = TargetVessel(-5, -1, 95, 12, 150)
tv4 = TargetVessel(-2, 5.7, 280, 2, 250)
#tv5 = TargetVessel(9, 0.5, 270, 5, 80)

state.add_own_vessel(ov)
state.add_target_vessel(tv1)
state.add_target_vessel(tv2)
state.add_target_vessel(tv3)
state.add_target_vessel(tv4)
#state.add_target_vessel(tv5)

path = "state/state.json"
state.write_state(path)

timesteps = 7
scale = 10
timefactor = 6

for i in range(timesteps):
    coll_parameters = calculate_state_collision_parameters(state.get_state())
    enc_situations = calculate_state_encounter_situations(coll_parameters)
    state.plot(scale, coll_parameters, enc_situations)
    print("Timestep: " + str(i + 1))
    print_collision_parameters(coll_parameters)
    state = state.next_state(timefactor)
