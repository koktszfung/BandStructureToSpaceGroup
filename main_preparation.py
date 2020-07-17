import os

import function_list


if __name__ == "__main__":
    for required_dir in ["list/", "list/actual/", "list/guess/", "state_dicts/"]:
        if not os.path.exists(required_dir):
            os.mkdir(required_dir)
            print(f"made dir \"{required_dir}\"")
        else:
            print(f"dir \"{required_dir}\"")

    # prepare input data # (Do this every time dataset is changed)
    function_list.create_valid_list_file(
        num_bands=100,
        in_data_dir="data/hs_data_2/",
        out_list_path="list/actual/valid_list.txt"
    )

    # prepare actual data # (Do this every time dataset is changed)
    function_list.create_actual_spacegroup_list_files(
        in_list_path="list/actual/valid_list.txt",
        out_list_path_format="list/actual/spacegroup_list_{}.txt"
    )

    function_list.create_actual_crystal_list_files(
        in_list_path="list/actual/valid_list.txt",
        out_list_path_format="list/actual/crystal_list_{}.txt"
    )
