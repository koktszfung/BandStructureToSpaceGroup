import numpy as np

import torch.nn.functional

import data_loader
import function_training
import function_list

import latticesystem
import function_analysis


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # prepare neural network
    validate_size = 0.1
    num_bands = 100
    hs_indices = [0, 1, 3, 4, 5, 7, 8, 13, 31, 34, 37]  # 11 hs points in Brillouin zone out of 40

    model = torch.nn.Sequential(
        torch.nn.LeakyReLU(),
        torch.nn.Linear(len(hs_indices)*num_bands, 300),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(300, 100),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(100, 7),
        torch.nn.LeakyReLU(),
    )
    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.75)
    criterion = torch.nn.CrossEntropyLoss()

    # prepare data
    def json2inputlabel(data_json):
        data_input_np = np.array(data_json["bands"])[:, hs_indices].flatten().T
        data_label_np = np.array([latticesystem.latticesystem_number(data_json["number"]) - 1])
        return data_input_np, data_label_np
    dataset = data_loader.AnyDataset(
        [f"list/actual/latticesystem_list_{lsnum}.txt" for lsnum in range(1, 8)],
        json2inputlabel, validate_size, shuffle=True
    )
    validate_loader, train_loader = data_loader.get_validate_train_loader(dataset, 32)

    # train
    function_training.validate_train_loop(
        device, model, optimizer, scheduler, criterion, validate_loader, train_loader,
        num_epoch=1, num_epoch_per_validate=5, state_dict_path="state_dicts/state_dict_bs2ls"
    )

    # apply
    function_list.create_any_guess_list_files(
        device, model, hs_indices, validate_size, num_group=7,
        in_list_paths=[f"list/actual/latticesystem_list_{lsnum}.txt" for lsnum in range(1, 8)],
        out_list_path_format="list/guess/latticesystem_list_{}.txt"
    )

    def json2inputlabel(data_json):
        data_label_np = np.array([latticesystem.latticesystem_number(data_json["number"]) - 1])
        return data_label_np
    function_analysis.plot_confusion(
        ["TRI", "MCL", "ORC", "TET", "RHL", "HEX", "CUB"],
        "list/guess/latticesystem_list_{}.txt", json2inputlabel
    )

    import winsound
    winsound.Beep(200, 500)


if __name__ == "__main__":
    main()
