import csv
import math
from openpyxl import Workbook
from openpyxl.styles import Border, Font, Side
from openpyxl.styles.numbers import BUILTIN_FORMATS

f_name = input('Введите название файла: ')
prof = input('Введите название профессии: ')
def read():
    with open(f_name, encoding='utf-8-sig') as r_file:
        file = csv.reader(r_file, delimiter=",")
        index = 0
        vacs = []
        header = []
        for i in file:
            if index == 0:
                l = len(i)
                index += 1
                header = i
            else:
                if len(i) != l or '' in i:
                    continue
                vacs.append(i)
        return vacs, header

vacs, header = read()

list = []
valute = {
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
}
for vac in vacs:
    salary_currency = vac[header.index('salary_currency')]
    salary_from = int(float(vac[header.index('salary_from')])) * valute[salary_currency]
    salary_to = int(float(vac[header.index('salary_to')])) * valute[salary_currency]
    name = vac[header.index('name')]
    area_name = vac[header.index('area_name')]
    published_at = vac[header.index('published_at')]
    a = [name, salary_from, salary_to, salary_currency, area_name, published_at]
    list.append(a)

def stat(vacs):
    zp_in_city = {}
    counter = {}
    zp = {}
    counter_vac = {}
    pr_counter = {}
    pr_zp = {}
    for vac in vacs:
        salary = (vac[1] + vac[2]) / 2
        if int(vac[-1][0:4]) not in counter_vac.keys():
            counter_vac[int(vac[-1][0:4])] = 1
        else:
            counter_vac[int(vac[-1][0:4])] += 1
        if vac[-1][0:4] not in zp.keys():
            zp[vac[-1][0:4]] = []
            zp[vac[-1][0:4]].append(salary)
        else:
            zp[vac[-1][0:4]].append(salary)
        if prof in vac[0]:
            if vac[-1][0:4] not in pr_zp.keys():
                pr_zp[vac[-1][0:4]] = []
                pr_zp[vac[-1][0:4]].append(salary)
            else:
                pr_zp[vac[-1][0:4]].append(salary)
            if int(vac[-1][0:4]) not in pr_counter.keys():
                pr_counter[int(vac[-1][0:4])] = 1
            else:
                pr_counter[int(vac[-1][0:4])] += 1
        if vac[-2] in counter:
            counter[vac[-2]] += 1
        else:
            counter[vac[-2]] = 1
        if vac[-2] in zp_in_city:
            zp_in_city[vac[-2]].append(salary)
        else:
            zp_in_city[vac[-2]] = []
            zp_in_city[vac[-2]].append(salary)
    if len(pr_counter.keys()) == 0:
        pr_counter = {2022: 0}
    din_zp = {}
    zp_din_pr = {}
    zp_city = {}
    counter_city = {}
    for x in counter:
        counter_city[x] = round(counter[x] / len(vacs), 4)
    for x in zp_in_city:
        if counter_city[x] >= 0.01:
            zp_city[x] = math.floor(sum(zp_in_city[x]) / len(zp_in_city[x]))
    for x in pr_zp:
        zp_din_pr[int(x)] = math.floor(sum(pr_zp[x]) / len(pr_zp[x]))
    for x in zp:
        din_zp[int(x)] = math.floor(sum(zp[x]) / len(zp[x]))

    if len(zp_din_pr.keys()) == 0:
        zp_din_pr = {2022: 0}
    return din_zp, counter_vac, zp_din_pr, pr_counter, zp_city, counter_city

a, b, c, d, e, f = stat(list)
e_sort = sorted(e.items(), key=lambda x: x[1], reverse=True)
e_sort = dict(e_sort)
f_sort = sorted(f.items(), key=lambda x: x[1], reverse=True)
f_sort = dict(f_sort)
e_new = {}
f_new = {}
i = 0
for x in e_sort:
    i += 1
    if i == 11:
        break
    e_new[x] = e_sort[x]

i = 0
for x in f_sort:
    i += 1
    if i == 11:
        break
    if f[x] >= 0.01:
        f_new[x] = f_sort[x]

print(f'Динамика уровня зарплат по годам: {a}')
print(f'Динамика количества вакансий по годам: {b}')
print(f'Динамика уровня зарплат по годам для выбранной профессии: {c}')
print(f'Динамика количества вакансий по годам для выбранной профессии: {d}')
print(f'Уровень зарплат по городам (в порядке убывания): {e_new}')
print(f'Доля вакансий по городам (в порядке убывания): {f_new}')

workbook = Workbook()
worksheet = workbook.active
worksheet.title = 'Статистика по годам'
worksheet.append({'A': 'Год', 'B': 'Средняя зарплата', 'C': f'Средняя зарплата - {prof}', 'D': 'Количество ваканский', 'E': f'Количество ваканский - {prof}'})
thin_bord = Side(color='000000', border_style='thin')

worksheet['A1'].font = Font(bold=True)
worksheet['A1'].border = Border(top=thin_bord, bottom=thin_bord, left=thin_bord, right=thin_bord)
worksheet['B1'].font = Font(bold=True)
worksheet['B1'].border = Border(top=thin_bord, bottom=thin_bord, left=thin_bord, right=thin_bord)
worksheet['C1'].font = Font(bold=True)
worksheet['C1'].border = Border(top=thin_bord, bottom=thin_bord, left=thin_bord, right=thin_bord)
worksheet['D1'].font = Font(bold=True)
worksheet['D1'].border = Border(top=thin_bord, bottom=thin_bord, left=thin_bord, right=thin_bord)
worksheet['E1'].font = Font(bold=True)
worksheet['E1'].border = Border(top=thin_bord, bottom=thin_bord, left=thin_bord, right=thin_bord)
worksheet.column_dimensions['A'].width = 5
worksheet.column_dimensions['B'].width = 17
worksheet.column_dimensions['C'].width = 20 + len(prof)
worksheet.column_dimensions['D'].width = 21
worksheet.column_dimensions['E'].width = 24 + len(prof)


for i, val in enumerate(a):
    worksheet.append([val, a[val], c[val], b[val], d[val]])
    worksheet[f'A{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
    worksheet[f'B{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
    worksheet[f'C{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
    worksheet[f'D{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
    worksheet[f'E{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)


worksheet_1 = workbook.create_sheet('Статистика по городам')
worksheet_1.append({'A': 'Город', 'B': 'Уровень зарплат', 'D': 'Город', 'E': 'Доля вакансий'})
worksheet_1['A1'].font = Font(bold=True)
worksheet_1['A1'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
worksheet_1['B1'].font = Font(bold=True)
worksheet_1['B1'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
worksheet_1['D1'].font = Font(bold=True)
worksheet_1['D1'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
worksheet_1['E1'].font = Font(bold=True)
worksheet_1['E1'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
worksheet_1.column_dimensions['A'].width = 20
worksheet_1.column_dimensions['B'].width = 16
worksheet_1.column_dimensions['C'].width = 1.29
worksheet_1.column_dimensions['D'].width = 20
worksheet_1.column_dimensions['E'].width = 14


newLen = 0
for i, val in enumerate(e_new):
    curLen = len(val)
    newLen = curLen if curLen > newLen else newLen
    worksheet_1.append([val, e_new[val]])
    worksheet_1[f'A{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
    worksheet_1[f'B{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
worksheet_1.column_dimensions['A'].width = newLen + 2

newLen = 0
for i, val in enumerate(f_new):
    curLen = len(val)
    newLen = curLen if curLen > newLen else newLen
    worksheet_1[f'D{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
    worksheet_1[f'E{i + 2}'].border = Border(top=thin_bord, left=thin_bord, bottom=thin_bord, right=thin_bord)
    worksheet_1[f'D{i + 2}'] = val
    worksheet_1[f'E{i + 2}'] = f_new[val]
    worksheet_1[f'E{i + 2}'].number_format = BUILTIN_FORMATS[10]
worksheet_1.column_dimensions['D'].width = newLen + 2

workbook.save('report.xlsx')