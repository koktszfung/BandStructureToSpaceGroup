import numpy as np

import torch.nn.functional

import data_loader
import function_training
import function_list


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # prepare neural network
    num_bands = 100
    hs_indices = [0, 1, 3, 4, 5, 7, 8, 13, 31, 34, 37]  # 11 hs points in Brillouin zone out of 40

    model = torch.nn.Sequential(
        torch.nn.LeakyReLU(),
        torch.nn.Linear(len(hs_indices)*num_bands, 100),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(100, 100),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(100, 230),
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

    dataset = data_loader.AnyDataset("list/actual/valid_list.txt", json2inputlabel)
    valid_loader, train_loader = data_loader.get_valid_train_loader(dataset, 32, 0.1)

    # train
    function_training.validate_train_loop(
        device, model, optimizer, scheduler, criterion, valid_loader, train_loader,
        num_epoch=1, num_epoch_per_valid=3, state_dict_path="state_dict/state_dict_bs2sg"
    )

    # apply
    function_list.create_guess_list_files(
        device, model, hs_indices, num_group=230,
        in_list_path="list/actual/valid_list.txt",
        out_list_path_format="list/guess/spacegroup_list_{}.txt"
    )

    import winsound
    winsound.Beep(200, 500)


if __name__ == "__main__":
    main()