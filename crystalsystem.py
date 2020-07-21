def crystalsystem_number(sgnum: int):
    for csnum, margin in enumerate([2, 15, 74, 142, 167, 194, 230]):
        if sgnum <= margin:
            return csnum + 1


def spacegroup_index_lower(csnum: int):
    margins = [2, 15, 74, 142, 167, 194, 230]
    lower = margins[csnum - 2] if csnum > 1 else 0
    return lower


def spacegroup_index_upper(csnum: int):
    margins = [2, 15, 74, 142, 167, 194, 230]
    upper = margins[csnum - 1]
    return upper


def spacegroup_number_range(csnum: int):
    return range(spacegroup_index_lower(csnum) + 1, spacegroup_index_upper(csnum) + 1)


def crystalsystem_sizes():
    return [2, 15, 74, 142, 167, 194, 230]
