# group_names = [
#     "1", r"$\bar1$",
#     "2", "m", r"$\frac{2}{m}$",
#     "222", "mm2", r"$\frac{2}{m}\frac{2}{m}\frac{2}{m}$",
#     "4", r"$\bar4$", r"$\frac{4}{m}$", "422", "4mm", r"$\bar42m$", r"$\frac{4}{m}\frac{2}{m}\frac{2}{m}$",
#     "3", r"$\bar3$", "32", "3m", r"$\bar3\frac{2}{m}$",
#     "6", r"$\bar6$", r"$\frac{6}{m}$", "622", "6mm", r"$\bar6m2$", r"$\frac{6}{m}\frac{2}{m}\frac{2}{m}$",
#     "23", r"$\frac{2}{m}\bar3$", "432", r"$\bar43m$", r"$\frac{4}{m}\bar3\frac{2}{m}$"
# ]

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

