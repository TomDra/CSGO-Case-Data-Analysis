import time
import os
import ast
from Prices import price_grabber as pg


def avg_revenue_per_case():
    probabilities = []
    skins = []
    cases = []
    if not os.path.exists('temp'):
        os.makedirs('temp')
    out_file = open('temp/values.txt', 'w+')
    inp_file = open('skins.txt', 'r')
    for i in inp_file.readlines():
        skins.append(i.replace('\n', ''))
    for skin in skins:
        cases.append(ast.literal_eval(skin)[0])
    cases = list(dict.fromkeys(cases))
    for case in cases:
        for i in range(0, len(skins)):
            if ast.literal_eval(skins[i])[0] == case:
                stat_trak_prob = float(ast.literal_eval(skins[i])[2][1].replace('NO PRICE', str(1500))) * ((1 / 10) * float(ast.literal_eval(skins[i])[3]))
                prob = float(ast.literal_eval(skins[i])[2][0].replace('NO PRICE', str(500))) * ((9 / 10) * float(ast.literal_eval(skins[i])[3]))
                probabilities.append([case, stat_trak_prob + prob])
    new_list = []
    case_prices = open('cases.txt', 'r')
    dic = '{'
    for case_price_line in case_prices.readlines():
        case_price_line = case_price_line.split(':::')
        dic = dic + f'"{case_price_line[0]}":"{case_price_line[1]}",'
    case_price_dic = ast.literal_eval((dic + '}').replace(',}', '}'))
    for case in cases:
        addition = 0
        for pro in probabilities:
            if pro[0] == case:
                addition = addition + pro[1]
        new_list.append([case, addition - 2.19 - float(case_price_dic[case])])
    inp_file.close()
    out_file.close()
    return new_list


def sort(unsorted_list):
    sorted_list = sorted(unsorted_list, key=lambda x: x[1])
    return sorted_list


def result_file_write(file_name, sorted_list):
    file = open(file_name, 'w+')
    for item in sorted_list:
        line = f'{item[0]} ~ {item[1]}\n'
        file.write(line)
    file.close()


if __name__ == '__main__':
    start_time = time.time()
    case_file = 'cases.txt'
    price_file = 'skins.txt'
    stash_ids = 'csgo_stash_ids.txt'
    result_file = 'results.txt'
    files = [case_file, price_file, stash_ids, result_file]
    pg.item_case_search(files)
    sorted_list = (sort(avg_revenue_per_case()))[::-1]
    print(sorted_list)
    result_file_write(result_file, sorted_list)
    print(f'Steam Case Calc took - {(time.time() - start_time) / 60} Mins')
    pg.archive(files)
