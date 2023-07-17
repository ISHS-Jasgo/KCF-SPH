import json
from datetime import datetime

file_path = "./ppldata.json"


def update(place, pplmin, pplmax):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    json_data = {}
    with open(file_path, "r", encoding='UTF-8') as json_file:
        json_data = json.load(json_file)

    if place not in json_data:
        json_data[place] = {}
    json_data[place][time] = {
        "PPL_MIN": pplmin,
        "PPL_MAX": pplmax
    }

    with open(file_path, 'w', encoding='UTF-8') as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)
