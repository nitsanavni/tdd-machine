def cell_dies(number_of_neighbours: int) -> bool:
    return number_of_neighbours < 2
def lives_on(num_neighbours: int) -> bool:
    return num_neighbours in [2, 3]
def dies_from_overpopulation(number_of_neighbours: int) -> bool:
    return number_of_neighbours > 3
