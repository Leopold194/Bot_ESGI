import json

def get_mess():

    with open("extra.json", "r") as ex:
        data = json.load(ex)

    return (data["mess"], data["channel"])

def save_mess(mess, channel):

    with open("extra.json", "r") as ex:
        data = json.load(ex)

    data["mess"] = mess
    data["channel"] = channel

    with open("extra.json", "w") as ex:
        json.dump(data, ex)

def check_date(date):

    try:
        date = date.split("/")
        if date[0] == "$cancel" or (1 <= int(date[0]) <= 31 and 1 <= int(date[1]) <= 12 and int(date[2]) >= 2022):
            return True
        else:
            return False
    except:
        return False

