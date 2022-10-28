

def define_encounter_situation(ts_Q, os_Q):

    encounter_situations = ["head-on",
                            "overtaking",
                            "overtaken",
                            "cross sb",
                            "cross ps",
                            "pass CPA"]

    if ((0 <= ts_Q <= 5.7) or (354.3 <= ts_Q <= 360)) and ((0 <= os_Q <= 5.7) or (354.3 <= os_Q <= 360)):
        return encounter_situations[0]

    elif (112.5 <= os_Q <= 247.5) and ((0 <= ts_Q <= 90) or (270 <= ts_Q <= 360)):
        return encounter_situations[1]

    elif (112.5 <= ts_Q <= 247.5) and ((0 <= os_Q <= 90) or (270 <= os_Q <= 360)):
        return encounter_situations[2]

    elif 0 <= ts_Q <= 112.5:
        return encounter_situations[3]

    elif 247.5 <= ts_Q <= 360:
        return encounter_situations[4]

    else:
        return None


def calculate_state_encounter_situations(collision_paramters, state):

    encounter_situations = []

    for i in range(len(collision_paramters)):
        ts_Q = (collision_paramters[i][1] - state["ownvessel"]["cog"] + 360) % 360
        os_Q = (((collision_paramters[i][1] + 180) % 360) - state["targetvessels"][i]["cog"] + 360) % 360# TODO: NOT CORRECT
        encounter = define_encounter_situation(ts_Q, os_Q)
        encounter_situations.append(encounter)

    return encounter_situations


