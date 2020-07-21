import numpy as np

import function_analysis
import crystalsystem
import latticesystem

if __name__ == '__main__':
    # function_analysis.print_result(
    #     group_numbers=range(1, 231),
    #     guess_list_dir="list/guess/",
    #     actual_list_dir="list/actual/",
    #     list_format="spacegroup_list_{}.txt"
    # )
    #
    # def json2inputlabel(data_json):
    #     data_label_np = np.array([data_json["number"] - 1])
    #     return data_label_np
    # function_analysis.get_confusion(range(1, 231), "list/guess/spacegroup_list_{}.txt", json2inputlabel)

    function_analysis.print_result(
        group_numbers=range(1, 8),
        guess_list_dir="list/guess/",
        actual_list_dir="list/actual/",
        list_format="crystalsystem_list_{}.txt"
    )

    def json2inputlabel(data_json):
        data_label_np = np.array([crystalsystem.crystalsystem_number(data_json["number"]) - 1])
        return data_label_np
    function_analysis.get_confusion(
        ["TRI", "MCL", "ORC", "TET", "TRG", "HEX", "CUB"], "list/guess/crystalsystem_list_{}.txt", json2inputlabel
    )

    # function_analysis.print_result(
    #     group_numbers=range(1, 8),
    #     guess_list_dir="list/guess/",
    #     actual_list_dir="list/actual/",
    #     list_format="latticesystem_list_{}.txt"
    # )
    #
    # def json2inputlabel(data_json):
    #     data_label_np = np.array([latticesystem.latticesystem_number(data_json["number"]) - 1])
    #     return data_label_np
    # function_analysis.get_confusion(
    #     ["TRI", "MCL", "ORC", "TET", "RHL", "HEX", "CUB"], "list/guess/latticesystem_list_{}.txt", json2inputlabel
    # )

    pass
