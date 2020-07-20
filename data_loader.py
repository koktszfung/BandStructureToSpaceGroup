import os
import json
import numpy as np

import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler


class AnyDataset(Dataset):
    def __init__(self, in_list_path, json2inputlabel):
        self.data_inputs = []
        self.data_labels = []
        if os.stat(in_list_path).st_size == 0:
            raise OSError("list is empty")

        file_names = np.loadtxt(in_list_path, "U90", ndmin=1)
        for i, file_name in enumerate(file_names):
            with open(file_name, "r") as file:
                data_json = json.load(file)
            # json2inputlabel is a function parsed to init, which handles a json dict and give input and label
            data_input_np, data_label_np = json2inputlabel(data_json)
            self.data_inputs.append(torch.from_numpy(data_input_np).float())
            self.data_labels.append(torch.from_numpy(data_label_np).long())
            print("\r\tload: {}/{}".format(i, len(file_names)), end="")
        print("\rload: {}".format(len(file_names)))

        self.len = len(self.data_inputs)

    def __len__(self):
        return self.len

    def __getitem__(self, index):
        return self.data_inputs[index], self.data_labels[index]


def get_validate_train_loader(dataset, batch_size, validate_size):
    num_train = len(dataset)
    indices = list(range(num_train))
    split = int(validate_size * num_train)

    validate_sampler = SubsetRandomSampler(indices[:split])
    train_sampler = SubsetRandomSampler(indices[split:])

    validate_loader = DataLoader(dataset, batch_size=batch_size, sampler=validate_sampler)
    train_loader = DataLoader(dataset, batch_size=batch_size, sampler=train_sampler)

    return validate_loader, train_loader
