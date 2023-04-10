import re
import csv


def get_data():
    n_txt = int(input('Количество файлов отчета: '))
    data = []
    data_head = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    os_list = [os_prod_list, os_name_list, os_code_list, os_type_list]
    for n in range(n_txt):
        with open(f'info_{n+1}.txt', 'r') as f:
            row = f.readlines()
            for k in range(len(data_head)):
                for n_row in range(len(row)):
                    if re.search(data_head[k], row[n_row]):
                        os = re.sub(data_head[k]+r':\s+', '', row[n_row], count=0)
                        os_list[k].append(os[:-1])
    data.append(data_head)
    for i in range(n_txt):
        row_data = []
        row_data.append(os_prod_list[i])
        row_data.append(os_name_list[i])
        row_data.append(os_code_list[i])
        row_data.append(os_type_list[i])
        data.append(row_data)
    return data


# Второй вариант решения
# def get_data():
#     n_txt = int(input('Количество файлов отчета: '))
#     data_head = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
#
#     data = [data_head]
#     for n in range(n_txt):
#         data.append([])
#         with open(f'info_{n+1}.txt', 'r') as f:
#             row = f.readlines()
#             for k in range(len(data_head)):
#                 for n_row in range(len(row)):
#                     if re.search(data[0][k], row[n_row]):
#                         os = re.sub(data_head[k]+r':\s+', '', row[n_row], count=0)
#                         data[n+1].append(os[:-1])
#     return data


def write_to_csv(name_csv):
    with open(f'{name_csv}.csv', 'w') as f_n:
        f_n_writer = csv.writer(f_n, quoting=csv.QUOTE_NONNUMERIC)
        data = get_data()
        for row in data:
            f_n_writer.writerow(row)
    with open(f'{name_csv}.csv') as f_n:
        print(f_n.read())


write_to_csv('test')
