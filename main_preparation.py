import os

import function_list

import crystalsystem
import latticesystem

if __name__ == "__main__":
    for required_dir in ["list/", "list/actual/", "list/guess/", "state_dicts/"]:
        if not os.path.exists(required_dir):
            os.mkdir(required_dir)
            print(f"made dir \"{required_dir}\"")
        else:
            print(f"dir \"{required_dir}\" exists")

    # prepare input data # (Do this every time dataset is changed)
    function_list.create_valid_list_file(
        num_bands=100,
        in_data_dir="data/hs_data_2/",
        out_list_path="list/valid_list.txt"
    )

    function_list.create_any_actual_list_files(
        num_groups=230, in_list_path="list/valid_list.txt",
        out_list_path_format="list/actual/spacegroup_list_{}.txt",
        sgnum2outnum=lambda sgnum: sgnum
    )

    function_list.create_any_actual_list_files(
        num_groups=7, in_list_path="list/valid_list.txt",
        out_list_path_format="list/actual/crystalsystem_list_{}.txt",
        sgnum2outnum=lambda sgnum: crystalsystem.crystalsystem_number(sgnum)
    )

    function_list.create_any_actual_list_files(
        num_groups=7, in_list_path="list/valid_list.txt",
        out_list_path_format="list/actual/latticesystem_list_{}.txt",
        sgnum2outnum=lambda sgnum: latticesystem.latticesystem_number(sgnum)
    )
