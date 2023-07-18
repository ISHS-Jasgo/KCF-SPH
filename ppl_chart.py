import matplotlib.pyplot as plt
import json
import numpy as np

plt.figure(dpi=300)


def ppl_data(key):
    file_path = "./ppldata.json"
    json_data = {}
    ppl_list = []
    with open(file_path, "r", encoding='UTF-8') as json_file:
        json_data = json.load(json_file)

    for time in json_data[key]:
        max_ppl = int(json_data[key][time]["PPL_MAX"])
        min_ppl = int(json_data[key][time]["PPL_MIN"])
        ppl_mean = (max_ppl + min_ppl) / 2
        ppl_list.append(ppl_mean)

    x = np.arange(0, len(ppl_list))
    plt.plot(x, ppl_list)
    plt.show()


def main():
    file_path = "./ppldata.json"
    json_data = {}
    ppl_list = []
    with open(file_path, "r", encoding='UTF-8') as json_file:
        json_data = json.load(json_file)

    for key in json_data:
        ppl_data(key)


if __name__ == "__main__":
    main()
