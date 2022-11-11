

def calculate_obstacle_priority(enc_situation, os_length, os_type, os_status, os_tss, os_nar_ch, os_res_vis,
                                ts_length, ts_type, ts_status, ts_tss, ts_nar_ch, ts_res_vis):

    # Give way priorities for OS and TS
    os_give_way = False
    ts_give_way = False

    priorities = ["PLANE", "POWER", "SAIL", "FISH", "CBD", "RAM", "NUC", "OBS"]

    if os_res_vis or ts_res_vis:
        os_give_way = True
        ts_give_way = True

    elif enc_situation == "overtaking":
        os_give_way = True
        ts_give_way = False

    elif enc_situation == "overtaken":
        os_give_way = False
        ts_give_way = True

    elif priorities.index(os_status) < priorities.index(ts_status):
        os_give_way = True
        ts_give_way = False

    elif enc_situation == "head-on":
        os_give_way = True
        ts_give_way = True

    elif enc_situation == "cross sb":
        os_give_way = True
        ts_give_way = False

    elif enc_situation == "cross ps":
        os_give_way = False
        ts_give_way = True

    return os_give_way, ts_give_way











