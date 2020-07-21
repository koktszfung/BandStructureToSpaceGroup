spacegroup_numbers = [
    # triclinic
    (1, 2),

    # monoclinic
    (3, 4,
     6, 7,
     10, 11,
     13, 14),  # P

    (5,
     8, 9,
     12,
     15),  # C

    # orthorhombic
    (*range(16, 20),
     *range(25, 35),
     *range(47, 63)),  # P

    (23, 24,
     44, 45, 46,
     *range(71, 75)),  # I

    (22,
     42, 43,
     69, 70),  # F

    (20, 21,
     *range(35, 42),
     *range(63, 69)),  # A or C

    # tetragonal
    (*range(75, 79),
     81,
     *range(83, 87),
     *range(89, 97),
     *range(99, 107),
     *range(111, 119),
     *range(123, 139)),  # P

    (79, 80,
     82,
     87, 88,
     97, 98,
     *range(107, 111),
     *range(119, 123),
     *range(139, 143)),  # I

    # trigonal
    (146,
     148,
     155,
     160, 161,
     166, 167),  # R

    (143, 144, 145,
     147,
     *range(149, 155),
     *range(156, 160),
     *range(162, 166)),  # P

    # hexagonal
    range(168, 195),

    # cubic
    (195,
     198,
     200, 201,
     205,
     207, 208,
     212, 213,
     215,
     218,
     *range(221, 225)),  # P

    (197,
     199,
     204,
     206,
     211,
     214,
     217,
     220,
     229, 230),  # I

    (196,
     202, 203,
     209, 210,
     216,
     219,
     *range(225, 229)),  # F

]


def bravaislattice_number(sgnum: int):
    for i, sgnums in enumerate(spacegroup_numbers):
        if sgnum in sgnums:
            return i + 1
