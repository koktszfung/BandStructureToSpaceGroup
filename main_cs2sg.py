import numpy as np

import torch.nn.functional

import data_loader
import function_training
import function_list

import crystal


def main_one(csnum):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # prepare neural network
    num_bands = 100
    hs_indices = [0, 1, 3, 4, 5, 7, 8, 13, 31, 34, 37]  # 11 hs points in Brillouin zone out of 40

    cs_sizes = crystal.crystal_system_sizes()
    output_sizes = cs_sizes[csnum - 1] - cs_sizes[csnum - 2] + 1 if csnum > 1 else 3

    model = torch.nn.Sequential(
        torch.nn.LeakyReLU(),
        torch.nn.Linear(len(hs_indices)*num_bands, 100),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(100, 100),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(100, output_sizes),
        torch.nn.LeakyReLU(),
    )
    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.75)
    criterion = torch.nn.CrossEntropyLoss()

    # prepare data
    crystal_upper = crystal.spacegroup_index_upper(csnum)
    crystal_lower = crystal.spacegroup_index_lower(csnum)
    crystal_size = crystal_upper - crystal_lower

    def json2inputlabel(data_json):
        data_input_np = np.array(data_json["bands"])[:, hs_indices].flatten().T
        sgnum = data_json["number"]
        if crystal_lower < sgnum - 1 < crystal_upper:
            data_label_np = np.array([sgnum - 1 - crystal_lower])
        else:
            data_label_np = np.array([crystal_size])
        return data_input_np, data_label_np

    dataset = data_loader.AnyDataset(f"list/guess/crystal_list_{csnum}.txt", json2inputlabel)
    valid_loader, train_loader = data_loader.get_valid_train_loader(dataset, 32, 0.1)

    # train
    function_training.validate_train_loop(
        device, model, optimizer, scheduler, criterion, valid_loader, train_loader,
        num_epoch=10, num_epoch_per_valid=3, state_dict_path="state_dict/state_dict_cs2sg"
    )

    # apply
    function_list.create_guess_list_files(
        device, model, hs_indices, num_group=230,
        in_list_path="list/actual/valid_list.txt",
        out_list_path_format="list/guess/spacegroup_list_{}.txt"
    )

    import winsound
    winsound.Beep(200, 500)


def main_all():
    for i in range(1, 8):
        main_one(i)


if __name__ == '__main__':
    main_all()
