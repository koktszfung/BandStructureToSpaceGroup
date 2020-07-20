def latticesystem_number(sg: int):
    for ls, margin in enumerate([2, 15, 74, 142, 149, 194, 230]):
        if sg <= margin:
            return ls + 1


def spacegroup_index_lower(ls: int):
    margins = [2, 15, 74, 142, 149, 194, 230]
    lower = margins[ls - 2] if ls > 1 else 0
    return lower


def spacegroup_index_upper(ls: int):
    margins = [2, 15, 74, 142, 149, 194, 230]
    upper = margins[ls - 1]
    return upper


def spacegroup_number_range(ls: int):
    return range(spacegroup_index_lower(ls) + 1, spacegroup_index_upper(ls) + 1)


def latticesystem_sizes():
    return [2, 15, 74, 142, 149, 194, 230]
