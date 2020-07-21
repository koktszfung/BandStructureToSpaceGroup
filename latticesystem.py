def latticesystem_number(sgnum: int):
    for lsnum, margin in enumerate([2, 15, 74, 142, 149, 194, 230]):
        if sgnum <= margin:
            return lsnum + 1


def spacegroup_index_lower(lsnum: int):
    margins = [2, 15, 74, 142, 149, 194, 230]
    lower = margins[lsnum - 2] if lsnum > 1 else 0
    return lower


def spacegroup_index_upper(lsnum: int):
    margins = [2, 15, 74, 142, 149, 194, 230]
    upper = margins[lsnum - 1]
    return upper


def spacegroup_number_range(lsnum: int):
    return range(spacegroup_index_lower(lsnum) + 1, spacegroup_index_upper(lsnum) + 1)


def latticesystem_sizes():
    return [2, 15, 74, 142, 149, 194, 230]
