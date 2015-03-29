from time import strftime, gmtime
import pandas as pd
import requests
import sys
import csv
import os


def write_regions_data():
    regions = ("0" + str(x) if x < 10 else str(x) for x in range(1, 28))
    urls = [None] * 25
    regions_new_format = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5}
    for x in regions:
        if int(x) not in regions_new_format:
            continue
        urls[regions_new_format[int(x)] - 1] = "http://www.star.nesdis.noaa.gov/smcd/emb/vci/gvix/G04/ts_L1/ByProvince/Mean/L1_Mean_UKR.R{}.txt".format(x)
    r = (str(requests.get(x).content).split('\\n')[1:-1] for x in urls)
    for x, k in enumerate(r):
        with open("VHI_{0}_{1}.csv".format(x + 1, strftime("%d", gmtime())), "w", newline='') as f:
            a = csv.writer(f, delimiter=',')
            data = [x.replace(' ', '').split(',') for x in k]
            a.writerows(data)


def get_results_from_df(df):
    year_vhi = zip(df["year"], df["VHI"])
    year_vhi1 = dict()
    for e in year_vhi:
        if not e[0] or e[1] < 0:
            continue
        if e[0] in year_vhi1:
            year_vhi1[e[0]].append(e[1])
        else:
            year_vhi1[e[0]] = [e[1]]
    min_max_year = [[x[0], min(x[1]), max(x[1])] for x in year_vhi1.items()]
    avg = [[x[0], sum(x[1]) / len(x[1])] for x in year_vhi1.items()]
    normal = list(filter(lambda x: 40 <= x[1] <= 60, avg))
    stress = list(filter(lambda x: x[1] < 40, avg))
    return min_max_year, avg, normal, stress


def read_everything_from_folder(path):
    if not os.path.isdir(path):
        print("No such directory")
        sys.exit()
    data_frames = list(map(lambda x: pd.read_csv(os.path.join(path, x)), os.listdir(path)))
    return data_frames


def main():
    x = read_everything_from_folder('data')
    all_data = map(get_results_from_df, x)


if __name__ == '__main__':
    main()
