import function_analysis

if __name__ == '__main__':
    # function_analysis.print_result(
    #     group_numbers=range(1, 231),
    #     guess_list_dir="list/guess/",
    #     actual_list_dir="list/actual/",
    #     list_format="spacegroup_list_{}.txt"
    # )
    function_analysis.print_result(
        group_numbers=range(1, 8),
        guess_list_dir="list/guess/",
        actual_list_dir="list/actual/",
        list_format="crystal_list_{}.txt"
    )
