import os
import json
import numpy as np

import torch

import crystal


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
        open(out_list_path_format.format(i+1), "w").close()


def create_actual_spacegroup_list_files(in_list_path, out_list_path_format, seed=None):
    create_empty_list_files(230, out_list_path_format)  # empty files for appending
    file_paths = np.loadtxt(in_list_path, "U90")
    if seed is not None:
        np.random.seed(seed)
    np.random.shuffle(file_paths)  # randomize order of data
    for i, file_path in enumerate(file_paths):
        with open(file_path, "r") as file:
            data_json = json.load(file)
        sgnum = data_json["number"]
        with open(out_list_path_format.format(sgnum), "a") as file_out:
            file_out.write(file_path + "\n")
        print("\r\tcreate actual list: {}/{}".format(i, len(file_paths)), end="")
    print("\rcreate actual list: {}".format(len(file_paths)))


def create_actual_crystal_list_files(in_list_path, out_list_path_format, seed=None):
    create_empty_list_files(7, out_list_path_format)
    file_paths = np.loadtxt(in_list_path, "U90")
    if seed is not None:
        np.random.seed(seed)
    np.random.shuffle(file_paths)  # randomize order of data
    for i, file_path in enumerate(file_paths):
        with open(file_path, "r") as file:
            data_json = json.load(file)
        csnum = crystal.crystal_number(data_json["number"])
        with open(out_list_path_format.format(csnum), "a") as file_out:
            file_out.write(file_path + "\n")
        print("\r\tcreate actual list: {}/{}".format(i, len(file_paths)), end="")
    print("\rcreate actual list: {}".format(len(file_paths)))


def create_guess_list_files(device, model, hs_indices, num_group, split, in_list_path, out_list_path_format):
    create_empty_list_files(num_group, out_list_path_format)
    file_paths = np.loadtxt(in_list_path, "U90")[:split]
    for i, file_path in enumerate(file_paths):
        with open(file_path, "r") as file:
            data_json = json.load(file)
        data_input_np = np.array(data_json["bands"])
        data_input_np = data_input_np[:, hs_indices].flatten().T
        data_input = torch.from_numpy(data_input_np).float()
        output = model(data_input.to(device))  # feed through the neural network
        sgnum = torch.max(output, 0)[1].item() + 1  # predicted with the most confidence
        with open(out_list_path_format.format(sgnum), "a") as file_out:
            file_out.write(file_path + "\n")
        print("\r\tcreate guess list: {}/{}".format(i, len(file_paths)), end="")
    print("\rcreate guess list: {}".format(len(file_paths)))


def append_guess_spacegroup_in_crystal_list_files(device, model, csnum, hs_indices, split,
                                                  in_list_path, out_list_path_format):
    if os.stat(in_list_path).st_size == 0:
        return
    file_paths = np.loadtxt(in_list_path, "U60")[:split]
    for i, file_path in enumerate(file_paths):
        with open(file_path, "r") as file:
            data_json = json.load(file)
        data_input_np = np.array(data_json["bands"])
        data_input_np = data_input_np[:, hs_indices].flatten().T
        data_input = torch.from_numpy(data_input_np).float()
        output = model(data_input.to(device))
        sgnum = torch.max(output, 0)[1].item() + 1 + crystal.spacegroup_index_lower(csnum)  # sgnum = output + lower(cs)
        if sgnum not in crystal.spacegroup_number_range(csnum):
            print("\r\tcreate guess list: {}/{}".format(i, len(file_paths)), end="")
            continue
        with open(out_list_path_format.format(sgnum), "a") as file_out:
            file_out.write(file_path + "\n")
        print("\r\tcreate guess list: {}/{}".format(i, len(file_paths)), end="")
    print("\rcreate guess list: {}".format(len(file_paths)))
