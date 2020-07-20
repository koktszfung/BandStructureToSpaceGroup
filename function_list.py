import os
import json
import numpy as np

import torch


def create_valid_list_file(num_bands, in_data_dir, out_list_path, seed=None):
    print("\tcreate valid list:", end="")
    valid_file_names = []
    for root, dirs, file_names in os.walk(in_data_dir):  # loop through file names in a directory
        for i, file_name in enumerate(file_names):
            with open(in_data_dir + file_name, "r") as file:
                data_json = json.load(file)
            if len(data_json["bands"]) != num_bands:  # accept only data with certain number of bands
                continue
            valid_file_names.append(file_name)
            print("\r\tcreate valid list: {}/{}".format(i, len(file_names)), end="")
    if seed is not None:
        np.random.seed(seed)
    np.random.shuffle(valid_file_names)  # randomize order of data
    with open(out_list_path, "w") as file_out:
        for file_name in valid_file_names:
            file_out.write(in_data_dir + file_name + "\n")  # write data_file_paths
    print("\rcreate valid list: {}".format(len(open(out_list_path).readlines())))


def create_empty_list_files(out_num_group, out_list_path_format):
    for i in range(out_num_group):
        open(out_list_path_format.format(i + 1), "w").close()


def create_any_actual_list_files(num_groups, in_list_path, out_list_path_format, sgnum2outnum, seed=None):
    create_empty_list_files(num_groups, out_list_path_format)  # empty files for appending
    file_paths = np.loadtxt(in_list_path, "U90")
    if seed is not None:
        np.random.seed(seed)
    np.random.shuffle(file_paths)  # randomize order of data
    for i, file_path in enumerate(file_paths):
        with open(file_path, "r") as file:
            data_json = json.load(file)
        sgnum = data_json["number"]
        outnum = sgnum2outnum(sgnum)
        with open(out_list_path_format.format(outnum), "a") as file_out:
            file_out.write(file_path + "\n")
        print("\r\tcreate actual list: {}/{}".format(i, len(file_paths)), end="")
    print("\rcreate actual list: {}".format(len(file_paths)))


def append_any_guess_list_files(device, model, hs_indices, num_group, split, in_list_path, out_list_path_format):
    file_paths = np.loadtxt(in_list_path, "U90")[:split]
    for i, file_path in enumerate(file_paths):
        with open(file_path, "r") as file:
            data_json = json.load(file)
        data_input_np = np.array(data_json["bands"])
        data_input_np = data_input_np[:, hs_indices].flatten().T
        data_input = torch.from_numpy(data_input_np).float()
        output = model(data_input.to(device))  # feed through the neural network
        outnum = torch.max(output, 0)[1].item() + 1  # predicted with the most confidence
        if outnum > num_group:
            continue
        with open(out_list_path_format.format(outnum), "a") as file_out:
            file_out.write(file_path + "\n")
        print("\r\tcreate guess list: {}/{}".format(i, len(file_paths)), end="")
    print("\rcreate guess list: {}".format(len(file_paths)))


def create_any_guess_list_files(device, model, hs_indices, num_group, split,
                                in_list_path, out_list_path_format):
    create_empty_list_files(num_group, out_list_path_format)
    append_any_guess_list_files(device, model, hs_indices, num_group, split, in_list_path, out_list_path_format)
