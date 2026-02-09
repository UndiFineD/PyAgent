# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VAREdit\infinity\utils\csv_util.py
import csv
import os
import os.path as osp

import numpy as np


def write_dicts2csv_file(input_dict_list, csv_filename):
    os.makedirs(osp.dirname(csv_filename), exist_ok=True)
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = input_dict_list[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(input_dict_list)
    print(f'"{csv_filename}" has been written.')


def load_csv_as_dicts(csv_filename):
    with open(csv_filename, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)
