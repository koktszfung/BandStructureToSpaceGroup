import os
import json
import numpy as np

import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler


class AnyDataset(Dataset):
    def __init__(self, in_list_paths, json2inputlabel, validate_size, shuffle: bool):
        validate_inputs = []
        validate_labels = []
        train_inputs = []
        train_labels = []
        if not isinstance(in_list_paths, list):  # if only one path is parsed
            in_list_paths = [in_list_paths]
        if shuffle:
            np.random.shuffle(in_list_paths)
        for i, in_list_path in enumerate(in_list_paths):
            if os.stat(in_list_path).st_size == 0:  # if file is empty
                continue
            file_names = np.loadtxt(in_list_path, "U90", ndmin=1)
            split = int(validate_size*len(file_names))
            for j, file_name in enumerate(file_names):
                with open(file_name, "r") as file:
                    data_json = json.load(file)
                # json2inputlabel is a function parsed to init, which handles a json dict and give input and label
                data_input_np, data_label_np = json2inputlabel(data_json)
                if j <= split:
                    validate_inputs.append(torch.from_numpy(data_input_np).float())
                    validate_labels.append(torch.from_numpy(data_label_np).long())
                else:
                    train_inputs.append(torch.from_numpy(data_input_np).float())
                    train_labels.append(torch.from_numpy(data_label_np).long())
            print("\r\tload: {}/{}".format(i, len(in_list_paths)), end="")
        print("\rload: {}".format(len(in_list_paths)))
        if len(train_inputs) == 0:
            raise OSError("input list file is empty")
        print(f"train: {len(train_inputs)}")
        print(f"validate: {len(validate_inputs)}")
        self.data_inputs = [*validate_inputs, *train_inputs]
        self.data_labels = [*validate_labels, *train_labels]
        self.len = len(self.data_inputs)
        self.split = int(validate_size * self.len)

    def __len__(self):
        return self.len

    def __getitem__(self, index):
        return self.data_inputs[index], self.data_labels[index]


def get_validate_train_loader(dataset, batch_size):
    validate_sampler = SubsetRandomSampler(range(dataset.split))
    train_sampler = SubsetRandomSampler(range(dataset.split, len(dataset)))
    validate_loader = DataLoader(dataset, batch_size=batch_size, sampler=validate_sampler)
    train_loader = DataLoader(dataset, batch_size=batch_size, sampler=train_sampler)

    return validate_loader, train_loader
