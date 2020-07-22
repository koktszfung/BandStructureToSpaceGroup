import numpy as np

import function_analysis
import crystalsystem
import bravaislattice

if __name__ == '__main__':
    # # space group
    # function_analysis.print_result(
    #     group_numbers=range(1, 231),
    #     guess_list_dir="list/guess/",
    #     actual_list_dir="list/actual/",
    #     list_format="spacegroup_list_{}.txt",
    #     validate_size=0.1
    # )
    #
    # def json2label(data_json):
    #     data_label_np = np.array([data_json["number"] - 1])
    #     return data_label_np
    # function_analysis.plot_confusion(range(1, 231), "list/guess/spacegroup_list_{}.txt", json2label)

    # # crystal system
    # function_analysis.print_result(
    #     group_numbers=range(1, 8),
    #     guess_list_dir="list/guess/",
    #     actual_list_dir="list/actual/",
    #     list_format="crystalsystem_list_{}.txt",
    #     validate_size=0.1
    # )
    #
    # def json2label(data_json):
    #     data_label_np = np.array([crystalsystem.crystalsystem_number(data_json["number"]) - 1])
    #     return data_label_np
    # function_analysis.plot_confusion(
    #     ["TRI", "MCL", "ORC", "TET", "TRG", "HEX", "CUB"], "list/guess/crystalsystem_list_{}.txt", json2label
    # )

    # bravais lattice
    function_analysis.print_result(
        group_numbers=range(1, 15),
        guess_list_dir="list/guess/",
        actual_list_dir="list/actual/",
        list_format="bravaislattice_list_{}.txt",
        validate_size=0.1
    )

    def json2label(data_json):
        data_label_np = np.array([bravaislattice.bravaislattice_number(data_json["number"]) - 1])
        return data_label_np
    function_analysis.plot_confusion(
        ["aP", "mP", "mS", "oP", "oS", "oI", "oF", "tP", "tI", "hR", "hP", "cP", "cI", "cF"],
        "list/guess/bravaislattice_list_{}.txt", json2label
    )

    pass
