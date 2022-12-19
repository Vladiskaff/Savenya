import csv
import math
import matplotlib.pyplot as plt
import numpy as np


def read():
    file = input('Введите название файла: ')
    with open(file, encoding='utf-8-sig') as r_file:
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
prof = input('Введите название профессии: ')
dlist = []
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
    dlist.append(a)

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

a, b, c, d, e, f = stat(dlist)
e_sort = sorted(e.items(), key=lambda x: x[1], reverse=True)
e_sort = dict(e_sort)
f_sort = sorted(f.items(), key=lambda x: x[1], reverse=True)
f_sort = dict(f_sort)
e_new = {}
f_new = {}
count = 0
for x in e_sort:
    count += 1
    if count == 11:
        break
    e_new[x] = e_sort[x]

count = 0
for x in f_sort:
    count += 1
    if count == 11:
        break
    if f[x] >= 0.01:
        f_new[x] = f_sort[x]

print(f'Динамика уровня зарплат по годам: {a}')
print(f'Динамика количества вакансий по годам: {b}')
print(f'Динамика уровня зарплат по годам для выбранной профессии: {c}')
print(f'Динамика количества вакансий по годам для выбранной профессии: {d}')
print(f'Уровень зарплат по городам (в порядке убывания): {e_new}')
print(f'Доля вакансий по городам (в порядке убывания): {f_new}')

head1 = list(a.keys())
data1 = list(a.values())
data11 = list(c.values())
data2 = list(b.values())
data21 = list(d.values())
head3 = list(e_new.keys())
head4 = list(f_new.keys())
data4 = list(f_new.values())
other = 1 - sum(data4)
head4.append('Другие')
data4.append(other)
data3 = list(e_new.values())

for i in range(len(head3)):
    head3[i] = head3[i].replace(' ', '\n')
    if '-' in head3[i]:
        index = head3[i].index('-')
        head3[i] = head3[i][0:index + 1] + '\n' + head3[i][index + 1:]

x = np.arange(len(head1))
w = 0.35

fig, ((axes, axes1), (axes2, axes3)) = plt.subplots(2, 2)
r1 = axes.bar(x - w / 2, data1, w, label='средняя з/п')
r2 = axes.bar(x + w / 2, data11, w, label=f'з/п {prof}')
axes.set_xticks(x, head1)
axes.set_xticklabels(head1, rotation=90, fontsize=8)
axes.legend(fontsize=8)
axes.grid(axis='y')
axes.set_title('Уровень зарплат по годам')
y_t = []
for i in axes.get_yticks():
    y_t.append(int(i))
axes.set_yticklabels(y_t, fontsize=8)



r3 = axes1.bar(x - w / 2, data2, w, label='Количество вакансий')
r4 = axes1.bar(x + w / 2, data21, w, label=f'Количество вакансий\n{prof}')
axes1.set_xticks(x, head1)
axes1.set_xticklabels(head1, rotation=90, fontsize=8)
axes1.legend(fontsize=8)
axes1.grid(axis='y')
axes1.set_title('Количество вакансий по годам')
y_t = []
for i in axes1.get_yticks():
    y_t.append(int(i))
axes1.set_yticklabels(y_t, fontsize=8)



y = np.arange(len(head3))
axes2.barh(y, data3, align='center')
axes2.set_yticks(y, head3, fontsize=6)
axes2.grid(axis='x')
x_t = []
for i in axes2.get_xticks():
    x_t.append(int(i))
axes2.set_xticklabels(x_t, fontsize=8)
axes2.set_title('Уровень зарплат по городам')

axes3.pie(data4, labels=head4, textprops={'fontsize': 6})
axes3.set_title('Доля вакансий по городам')

fig.tight_layout()
plt.savefig('graph.png')
plt.show()