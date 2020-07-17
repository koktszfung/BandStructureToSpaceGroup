import torch
import function_list

import crystal


def main_one(csnum):
    num_bands = 100
    hs_indices = [0, 1, 3, 4, 5, 7, 8, 13, 31, 34, 37]  # 11 hs points in Brillouin zone out of 40

    cs_sizes = crystal.crystal_system_sizes()
    output_size = cs_sizes[csnum - 1] - cs_sizes[csnum - 2] + 1 if csnum > 1 else 3

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = torch.nn.Sequential(
        torch.nn.LeakyReLU(),
        torch.nn.Linear(len(hs_indices)*num_bands, 100),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(100, 100),
        torch.nn.LeakyReLU(),
        torch.nn.Linear(100, output_size),
        torch.nn.LeakyReLU(),
    )
    state_dict = torch.load("state_dicts/state_dict_cs2sg")
    model.load_state_dict(state_dict)
    model.eval()
    model = model.to(device)

    # apply
    function_list.append_guess_spacegroup_in_crystal_list_files(
        device, model, csnum, hs_indices,
        in_list_path="list/actual/valid_list.txt",
        out_list_path_format="list/guess/spacegroup_list_{}.txt"
    )


if __name__ == '__main__':
    function_list.create_empty_list_files(230, out_list_path_format="list/guess/spacegroup_list_{}.txt")
    for i in range(1, 8):
        main_one(csnum=i)
