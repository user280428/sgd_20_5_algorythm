from lg5 import lerch
from colour import dir_maker, colorer_2, list_maker



# Наш градиент из 30 цветов (надеюсь хватит)
colours = ['562929', '5d2e2c', '65332e', '6c3830', '743d33',
           '7b4335', '824936', '894f38', '90553a', '965b3b',
           '9d623d', 'a3683e', 'a96f40', 'af7641', 'b47d43',
           'b98544', 'be8c45', 'c39447', 'c79c49', 'cba44b',
           'cfac4d', 'd2b44f', 'd5bd52', 'd7c555', 'd9ce58',
           'dbd65c', 'dcdf60', 'dde865', 'def16a', 'defa70']



if __name__ == "__main__":
    # Алгоритм
    lerch()
    # Раскраска
    colorer_2(colours, list_maker(dir_maker()))

