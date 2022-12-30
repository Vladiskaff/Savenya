import csv

def filter_years(vacs, header, filter):
    '''
    Данная функия разделяет выгрузку данных на чанки по годам и сохраняет полученные файлы в отдельную папку
    Attributes:
        vacs(str): массив с полученными данными из файла
        header(str): массив с заголовками файла
        filter(dict): полученный словарь с годами
    '''
    for year in filter.keys():
        with open(f'3.2.1_list/{year}_vacancies.csv', 'w', encoding='utf-8-sig') as f:
            end = csv.writer(f)
            end.writerow(header)
            for i in vacs:
                if i[-1][0:4] == year:
                    end.writerow(i)

def read():
    '''
        Функция для считывания CSV-файла
        Returns:
            vacs(str): получает массив с вакансиями
        Array:
            header(str):получает шапку таблицы

    '''
    with open(input('Введите название файла: '), encoding='utf-8-sig') as r_file:
        file = csv.reader(r_file, delimiter=",")
        vacs = []
        header = []
        filter = {}
        index = 0
        for line in file:
            if index == 0:
                lenLine = len(line)
                index += 1
                header = line
            else:
                if len(line) != lenLine or '' in line:
                    continue
                vacs.append(line)
                year = line[-1][0:4]
                if year not in filter.keys():
                    filter[year] = 1
                else:
                    filter[year] += 1
        return vacs, header, filter

vacs, header, filter = read()
filter_years(vacs, header, filter)

