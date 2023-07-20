import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import colab

file_path = "./data2.json"

ppl_list = []
ppl_list_time = []
json_data = {}
with open(file_path, "r", encoding='UTF-8') as json_file:
    json_data = json.load(json_file)

for key in json_data:
    place_data = json_data[key]
    for key2 in place_data:
        time_data = place_data[key2]
        min = int(place_data[key2]['PPL_MIN'])
        max = int(place_data[key2]['PPL_MAX'])
        p=(min+max)/2
        ppl_list.append(p)
        ppl_list_time.append(key2)
    plt.plot(ppl_list_time,ppl_list)
    plt.show