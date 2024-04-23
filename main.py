from lg5 import lerch
from colour import dir_maker, colorer_2, list_maker






if __name__ == "__main__":
    # Алгоритм
    lerch()
    # Раскраска
    colorer_2(list_maker(dir_maker())[1], list_maker(dir_maker())[0])

