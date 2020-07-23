import numpy as np
import matplotlib.pyplot as plt

import function_analysis
import crystalsystem
import bravaislattice
import arithmeticcrystalclass
import pointgroup

if __name__ == '__main__':
    # crystal system
    function_analysis.print_result(
        group_numbers=range(1, 8),
        guess_list_dir="list/guess/",
        actual_list_dir="list/actual/",
        list_format="crystalsystem_list_{}.txt",
        validate_size=0.1
    )

    def json2label(data_json):
        data_label_np = np.array([crystalsystem.crystalsystem_number(data_json["number"]) - 1])
        return data_label_np
    plt.subplot(231)
    function_analysis.plot_confusion(
        json2label,
        [f"list/guess/crystalsystem_list_{i}.txt" for i in range(1, 8)],
        group_names=["TRI", "MCL", "ORC", "TET", "TRG", "HEX", "CUB"],
        show_text=False
    )
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.text(0.5, 1.02, "crystal system", horizontalalignment='center', fontsize=15, transform=plt.gca().transAxes)

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
    plt.subplot(232)
    function_analysis.plot_confusion(
        json2label,
        [f"list/guess/bravaislattice_list_{i}.txt" for i in range(1, 15)],
        group_names=["aP", "mP", "mS", "oP", "oS", "oI", "oF", "tP", "tI", "hR", "hP", "cP", "cI", "cF"],
        show_text=False
    )
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.text(0.5, 1.02, "bravais lattice", horizontalalignment='center', fontsize=15, transform=plt.gca().transAxes)

    # point group
    function_analysis.print_result(
        group_numbers=range(1, 33),
        guess_list_dir="list/guess/",
        actual_list_dir="list/actual/",
        list_format="pointgroup_list_{}.txt",
        validate_size=0.1
    )

    def json2label(data_json):
        data_label_np = np.array([pointgroup.pointgroup_number(data_json["number"]) - 1])
        return data_label_np
    plt.subplot(233)
    function_analysis.plot_confusion(
        json2label,
        [f"list/guess/pointgroup_list_{i}.txt" for i in range(1, 33)],
        show_text=False
    )
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.text(0.5, 1.02, "point group", horizontalalignment='center', fontsize=15, transform=plt.gca().transAxes)

    # arithmetic crystal class
    function_analysis.print_result(
        group_numbers=range(1, 74),
        guess_list_dir="list/guess/",
        actual_list_dir="list/actual/",
        list_format="arithmeticcrystalclass_list_{}.txt",
        validate_size=0.1
    )

    def json2label(data_json):
        data_label_np = np.array([arithmeticcrystalclass.arithmeticcrystalclass_number(data_json["number"]) - 1])
        return data_label_np
    plt.subplot(234)
    function_analysis.plot_confusion(
        json2label,
        [f"list/guess/arithmeticcrystalclass_list_{i}.txt" for i in range(1, 74)],
        show_text=False
    )
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.text(0.5, 1.02, "arithmetic crystal class",
             horizontalalignment='center', fontsize=15, transform=plt.gca().transAxes)

    # space group
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
    plt.subplot(235)
    function_analysis.plot_confusion(
        json2label,
        [f"list/guess/spacegroup_list_{i}.txt" for i in range(1, 231)],
        show_text=False
    )
    plt.gca().invert_yaxis()
    plt.gca().xaxis.set_ticks_position('bottom')
    plt.text(0.5, 1.02, "space group", horizontalalignment='center', fontsize=15, transform=plt.gca().transAxes)

    plt.show()
