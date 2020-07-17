import numpy as np

import torch.nn.functional

import data_loader
import function_training
import function_list

import crystal


def main_one(csnum):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # prepare neural network
    validate_size = 0.1
    num_bands = 100
    hs_indices = [0, 1, 3, 4, 5, 7, 8, 13, 31, 34, 37]  # 11 hs points in Brillouin zone out of 40

    cs_sizes = crystal.crystal_system_sizes()
    output_sizes = cs_sizes[csnum - 1] - cs_sizes[csnum - 2] + 1 if csnum > 1 else 3

    model = torch.nn.Sequential(
        torch.nn.LeakyReLU(),
        torch.nn.Linear(len(hs_indices)*num_bands, 300),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(300, 100),
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

    dataset = data_loader.AnyDataset(f"list/actual/crystal_list_{csnum}.txt", json2inputlabel)
    validate_loader, train_loader = data_loader.get_validate_train_loader(dataset, 32, validate_size)

    # train
    function_training.validate_train_loop(
        device, model, optimizer, scheduler, criterion, validate_loader, train_loader,
        num_epoch=1, num_epoch_per_validate=5, state_dict_path=f"state_dicts/state_dict_cs2sg_{csnum}"
    )

    # apply
    function_list.append_guess_spacegroup_in_crystal_list_files(
        device, model, csnum, hs_indices, split=int(validate_size*len(dataset)),
        in_list_path=f"list/actual/crystal_list_{csnum}.txt",
        out_list_path_format="list/guess/spacegroup_list_{}.txt"
    )

    import winsound
    winsound.Beep(200, 500)


if __name__ == '__main__':
    function_list.create_empty_list_files(230, out_list_path_format="list/guess/spacegroup_list_{}.txt")
    for i in range(1, 8):
        main_one(i)
