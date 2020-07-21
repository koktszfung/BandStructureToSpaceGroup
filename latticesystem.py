def latticesystem_number(sgnum: int):
    for lsindex, margin in enumerate([2, 15, 74, 142, 149, 194, 230]):
        if sgnum <= margin:
            return lsindex + 1
