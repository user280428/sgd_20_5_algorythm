import pandas as pd

def lerch():
    print('угол откоса должен быть равен 35, 45 ,55 или 65')
    angle = 45#int(input("угол откоса: "))
    while angle != 35 and angle != 45 and angle != 55 and angle != 65:
        angle = int(input("угол откоса: "))

    completion = 0
    iteration = 0
    #v - 1 коэф. для z
    #vv = 2 коэф. для z
    #vvv = 3 коэф. для z
    #c = коэф. для х
    #cc = коэф. для первого исключения
    #ссс = вспомогательный коэф. для сс
    if angle == 35:
        v,vv, vvv, c, cc, ссс = 2, 4, 7, 1, 3, 0
    elif angle == 55:
        v,vv, vvv, c, cc, ссс = 4, 7, 10, -1, 0, 1
    # загружаю библеотеку пандас для работы с таблицами эксель
    # таблицу эксель перевожу в формат датафрейм
    # значения датафрейма представляю в виде массива array
    df = pd.read_excel("контуры\\контур00.xlsx", header=None)
    mas = df.values
    sub_block = 2 #int(input("деление блоков: "))
    performance = 0/(sub_block**2)#int(input("минимальная эффективность: "))
    mas1 = []
    mas2 = []
    mas3 = []
    for i in range(len(mas)):
        for j in range(len(mas[i])):
            numb = 0
            while numb != sub_block:
                numb += 1
                mas1.append(mas[i,j]/(sub_block**2))
        mas2.append(mas1)
        mas1 = []
    for i in range(len(mas2)):
        numb = 0
        while numb != sub_block:
            numb += 1
            mas3.append(mas2[i])

    df = pd.DataFrame(mas3)
    df.to_excel("контуры\\контур0.xlsx", header=None, index=False)

    while completion == 0:
        iteration += 1
        df = pd.read_excel(f"контуры\\контур{iteration-1}.xlsx", header=None)
        array = df.values
        # profit - список который включает в себя сумму всех блоков в конусе (вес конуса), для каждого нижнего положительного блока (gain) по очереди
        # cache - список который записывает значения всех profit
        # journal - список который включает в себя [номер итерацииx, значение блока для которого проводится вычисление, номер строки, номер столбца]
        profit = [0]
        cache = []
        journal = []
        expenses = 0            # расходы
        revenue = 0             # выручка
        number_of_blocks = 0    # число блоков
        # a,b,о используются в цикле, предназначены для отслеживания строки,столбца и индекса ячейки
        # z,x,c,t,r используются в цикле, чтобы учесть особенности контура карьера при разных углах откоса
        a = 0
        o = 0
        z = 0
        # перебираю каждое значение массива (array), чтобы найти все положительные блоки (gain)
        # если значение блока больше 0, доабавляю его в список gain, фиксирую данные в журнал и считаю для этого значения вес конуса
        for i in array:
            b = 0
            a += 1
            for j in i:
                b += 1
                if j > 0:
                    bb=b
                    aa=a
                    journal += [[o,j,a,b]]
                    o += 1
        # этот цикл нужен для того чтобы посчитать вес конуса
        # сохраняем вес блока profit в списке cache
        # если при добыче блока, контур карьера выходит за границы лицензионного участка, вес конуса принимаем равным -123456789 и пропускаем его
                    x = 0
                    t = 0
                    r = 0
                    n_o_b = 0
                    for n in range(aa):
                        profit += array[aa - n - 1, bb - 1]
                        if array[aa - n - 1, bb - 1] == 0:
                            n_o_b -= 1
                        n_o_b += 1
                        #print('')
                        #print(f"\033[95m{n}\033[0m",end=',')
                        #print(array[aa - n - 1, bb - 1],end=',')
                        if angle == 35 or angle == 55:
                            if n < cc:
                                z = 0+ссс
                            if n == cc:
                                z = 1+ссс
                            z += 1
                            if z == v or z == vv or z == vvv:
                                x += c
                                #print(f"\033[92m{x}\033[0m", end=',')
                            if z == vvv:
                                z = 0
                            #print(f"\033[93m{z}\033[0m",end=',')
                        if angle == 65:
                            if n == 0:
                                x = 1
                            x -= 1
                            if z == 3 and t == 0:
                                z = 0
                                t += 1
                                x += 1
                            if t != 0:
                                if z == 2:
                                    z = 0
                                    t += 1
                                    x += 1
                            z += 1
                            if t == 6 + r:
                                t = 0
                                r += 1
                            #print(f"\033[91m{t}\033[0m", end=',')
                            #print(f"\033[92m{x}\033[0m", end=',')
                            #print(f"\033[93m{z}\033[0m",end=',')
                        for m in range(n + 1 + x):
                            try:
                                if m != 0:
                                    profit += array[aa - n - 1, bb - m - 1]
                                    profit += array[aa - n - 1, bb + m - 1]
                                    if array[aa - n - 1, bb - m - 1] == 0:
                                        n_o_b -= 1
                                    if array[aa - n - 1, bb + m - 1] == 0:
                                        n_o_b -= 1
                                    n_o_b += 2
                                    #print(array[aa - n - 1, bb - m - 1], end=',')
                                    #print(array[aa - n - 1, bb + m - 1], end=',')
                            except:
                                profit = -123456789

                    z = 0
                    x = 0
                    #print('')
                    #print(profit, aa, bb)
                    cache += [profit/n_o_b]
                    profit = [0]
                    n_o_b = 0
        # вывожу данные из журнала для навигации
        # print(cache.index(max(cache)),  '- индекс максимального числа cache')
        # print(journal[cache.index(max(cache))], '- данные журнала для максимального числа cache')
        if max(cache)[0] < performance:
            cache = -987654321
        # проверяю условия перед построением конуса
        # если значение прибыли меньше 0 или отработка блока возможна только при выходе за границы лицензии, продолжать работу алгоритма нет смысла
        # в противном случае создаем новую таблицу эксель,где посчитанный конус извлекается (все значения входящих ячеек в конус заменяются на 0)
        if cache == -123456789:
            print(f"\033[95mКонтур выходит за границы участка, добыча невозможна\033[0m")
            completion = 1
        elif cache == -987654321:
            print(f"\033[95mОтработка конуса не эффективна\033[0m")
            completion = 1
        elif max(cache)[0] < 0:
            print(f"\033[95mОтрицательная прибыль\033[0m")
            completion = 1
        else:
        # определяем координаты нижнего блока (записываем как ааа и bbb)
        # создаем копию исходной таблицы чтобы менять в ней значения
        # в цикле меняем значения ячеек конуса на 0 т.к. предполагаем что этот объем будет извлечен
        # попутно с этим считаем сумму всех отрицательных ячеек (expenses - расходы)
        # попутно с этим считаем сумму извлекаемых ячеек (number_of_blocks - число блоков)
        # создаем обновленную таблицу эксель
            result = journal[cache.index(max(cache))]
            aaa = result[2]-1
            bbb = result[3]-1
            df_copy = df.copy()
            t = 0
            r = 0
            for i in range(aaa+1):
                if df_copy.at[aaa-i,bbb] < 0:
                    expenses += df_copy.at[aaa-i,bbb]
                if df_copy.at[aaa-i,bbb] != 0:
                    number_of_blocks += 1
                if df_copy.at[aaa-i,bbb] > 0:
                    revenue += df_copy.at[aaa-i,bbb]
                df_copy.at[aaa-i,bbb] = 0

                if angle == 35 or angle == 55:
                    if i < cc:
                        z = 0+ссс
                    if i == cc:
                        z = 1+ссс
                    z += 1
                    if z == v or z == vv or z == vvv:
                        x += c
                    if z == vvv:
                        z = 0
                if angle == 65:
                    if i == 0:
                        x = 1
                    x -= 1
                    if z == 3 and t == 0:
                        z = 0
                        t += 1
                        x += 1
                    if t != 0:
                        if z == 2:
                            z = 0
                            t += 1
                            x += 1
                    z += 1
                    if t == 6 + r:
                        t = 0
                        r += 1

                for j in range(i+1+x):
                    if j != 0:
                        if df_copy.at[aaa - i, bbb - j] < 0:
                            expenses += df_copy.at[aaa - i, bbb - j]
                        if df_copy.at[aaa - i, bbb + j] < 0:
                            expenses += df_copy.at[aaa - i, bbb + j]
                        if df_copy.at[aaa - i, bbb - j] != 0:
                            number_of_blocks += 1
                        if df_copy.at[aaa - i, bbb + j] != 0:
                            number_of_blocks += 1
                        if df_copy.at[aaa - i, bbb - j] > 0:
                            revenue += df_copy.at[aaa - i, bbb - j]
                        if df_copy.at[aaa - i, bbb + j] > 0:
                            revenue += df_copy.at[aaa - i, bbb + j]
                        df_copy.at[aaa - i, bbb - j] = 0
                        df_copy.at[aaa - i, bbb + j] = 0
            print(number_of_blocks, f"\033[93m- число блоков\033[0m")
            print(expenses, f"\033[93m- расходы\033[0m")
            print(revenue, f"\033[93m- доходы\033[0m")
            df_copy.to_excel(f"контуры\\контур{iteration}.xlsx", index=False, header=None)
        print(revenue + expenses, f"\033[93m- прибыль\033[0m")
        try:
            print(int((revenue + expenses)/number_of_blocks), f"\033[93m- эффективность\033[0m")
        except:
            print('0 блоков')



        # report - файл отчета
        # добавляем данные в отчет
        # проверяю был ли построен конус
        # если конус не существует, указываю причину
        # если конус существует, вывожу его параметры в отчет
        # сохраняем данные в файл Excel (Отчет)
        # дополняем данные в существующей таблице, если это не первая итерация
        Report = pd.read_excel('Отчет.xlsx')

        if cache == -987654321:
            new_data = pd.DataFrame({
                'Доходы': [f'Отработка конуса не эффективна - {angle}']
            })
        elif max(cache)[0] == -123456789:
            new_data = pd.DataFrame({
                'Доходы': ['Контур выходит за границы участка, добыча невозможна']
            })
        elif max(cache)[0] < 0:
            new_data = pd.DataFrame({
                'Доходы': [f'Отрицательная прибыль Угол - {angle}']
            })
        else:
            new_data = pd.DataFrame({
                'Номер контура': [iteration],
                'Доходы': [revenue],
                'Расходы': [expenses],
                'Прибль': [revenue + expenses],
                'Число блоков': [number_of_blocks/(sub_block**2)],
                'Эффективность': [int((revenue + expenses)/(number_of_blocks/(sub_block**2)))],
                'Журнал': [journal[cache.index(max(cache))]]
            })
        updated_report = pd.concat([Report, new_data], ignore_index=True)
        updated_report.to_excel('Отчет.xlsx', index=False)

lerch()