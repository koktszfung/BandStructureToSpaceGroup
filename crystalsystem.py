def crystalsystem_number(sg: int):
    for cs, margin in enumerate([2, 15, 74, 142, 167, 194, 230]):
        if sg <= margin:
            return cs + 1


def spacegroup_index_lower(cs: int):
    margins = [2, 15, 74, 142, 167, 194, 230]
    lower = margins[cs - 2] if cs > 1 else 0
    return lower


def spacegroup_index_upper(cs: int):
    margins = [2, 15, 74, 142, 167, 194, 230]
    upper = margins[cs - 1]
    return upper


def spacegroup_number_range(cs: int):
    return range(spacegroup_index_lower(cs) + 1, spacegroup_index_upper(cs) + 1)


def crystalsystem_sizes():
    return [2, 15, 74, 142, 167, 194, 230]
