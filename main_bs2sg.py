import numpy as np

import torch.nn.functional

import data_loader
import function_training
import function_list

import function_analysis


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # prepare neural network
    validate_size = 0.1
    num_bands = 100
    hs_indices = range(48)

    model = torch.nn.Sequential(
        torch.nn.LeakyReLU(),
        torch.nn.Linear(len(hs_indices)*num_bands, 1000),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(1000, 250),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(250, 231),
        torch.nn.LeakyReLU(),
    )
    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.75)
    criterion = torch.nn.CrossEntropyLoss()

    # prepare data
    def json2inputlabel(data_json):
        data_input_np = np.array(data_json["bands"])[:, hs_indices].flatten().T
        data_label_np = np.array([data_json["number"] - 1])
        return data_input_np, data_label_np

    dataset = data_loader.AnyDataset(
        [f"list/actual/spacegroup_list_{sgnum}.txt" for sgnum in range(1, 231)],
        json2inputlabel, validate_size
    )
    validate_loader, train_loader = data_loader.get_validate_train_loader(dataset, 32)

    # train
    function_training.validate_train_loop(
        device, model, optimizer, scheduler, criterion, validate_loader, train_loader,
        num_epoch=20, num_epoch_per_validate=5, state_dict_path="state_dicts/state_dict_bs2sg"
    )

    # apply
    function_list.create_any_guess_list_files(
        device, model, hs_indices, validate_size, num_group=230,
        in_list_paths=[f"list/actual/spacegroup_list_{sgnum}.txt" for sgnum in range(1, 231)],
        out_list_path_format="list/guess/spacegroup_list_{}.txt"
    )

    import winsound
    winsound.Beep(200, 500)

    # analyse
    function_analysis.print_result(
        group_numbers=range(1, 231),
        guess_list_dir="list/guess/",
        actual_list_dir="list/actual/",
        list_format="spacegroup_list_{}.txt",
        validate_size=0.1
    )

    def json2label(data_json):
        data_label_np = np.array([data_json["number"] - 1])
        return data_label_np
    function_analysis.show_confusion(
        json2label,
        [f"list/guess/pointgroup_list_{i}.txt" for i in range(1, 231)],
    )


if __name__ == "__main__":
    main()
