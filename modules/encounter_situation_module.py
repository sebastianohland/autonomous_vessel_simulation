

def calculate_encounter_situation(Q, Q1, tcpa):

    encounter_situations = ["head-on",
                            "overtaking",
                            "overtaken",
                            "cross sb",
                            "cross ps",
                            "passed CPA"]

    # TODO: check rules for encounter situations
    # TODO: add rule so that encounter situation does not change during ongoing situation

    if tcpa < 0:
        return encounter_situations[5]

    if ((0 <= Q <= 5.7) or (354.3 <= Q <= 360)) and ((0 <= Q1 <= 5.7) or (354.3 <= Q1 <= 360)):
        return encounter_situations[0]

    elif (112.5 <= Q1 <= 247.5) and ((0 <= Q <= 90) or (270 <= Q <= 360)):
        return encounter_situations[1]

    elif (112.5 <= Q <= 247.5) and ((0 <= Q1 <= 90) or (270 <= Q1 <= 360)):
        return encounter_situations[2]

    elif 0 <= Q <= 112.5:
        return encounter_situations[3]

    elif 247.5 <= Q <= 360:
        return encounter_situations[4]

    else:
        return None


def calculate_state_encounter_situations(state_collision_parameters):

    encounter_situations = []

    for collision_parameters in state_collision_parameters:
        Q = collision_parameters[5]
        Q1 = collision_parameters[6]
        tcpa = collision_parameters[2]
        encounter = calculate_encounter_situation(Q, Q1, tcpa)
        encounter_situations.append(encounter)

    return encounter_situations


