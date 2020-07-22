spacegroup_numbers = [
    (1,),
    (2,),

    (3, 4, 5),
    range(6, 10),
    range(10, 16),

    range(16, 25),
    range(25, 47),
    range(47, 75),

    range(75, 81),
    (81, 82),
    range(83, 89),
    range(89, 99),
    range(99, 111),
    range(111, 123),
    range(123, 143),

    range(143, 147),
    (147, 148),
    range(149, 156),
    range(156, 162),
    range(162, 168),

    range(168, 174),
    (174,),
    (175, 176),
    range(177, 183),
    range(183, 187),
    range(187, 191),
    range(191, 195),

    range(195, 200),
    range(200, 207),
    range(207, 215),
    range(215, 221),
    range(221, 231),
]


def pointgroup_number(sgnum: int):
    for i, sgnums in enumerate(spacegroup_numbers):
        if sgnum in sgnums:
            return i + 1
