import time
import os
import ast

def avg_revenue_per_case():
    probabilities = []
    skins = []
    cases = []
    if not os.path.exists('temp'):
        os.makedirs('temp')
    out_file = open('temp/values.txt','w+')
    inp_file = open('current/skins.txt','r')
    for i in inp_file.readlines():
        skins.append(i.replace('\n',''))
    for skin in skins:
        cases.append(ast.literal_eval(skin)[0])
        #print(skin)
    cases = list(dict.fromkeys(cases))
    for case in cases:
        for i in range(0,len(skins)):
            if ast.literal_eval(skins[i])[0] == case:
                stat_trak_prob = float(ast.literal_eval(skins[i])[2][1].replace('NO PRICE',str(1500))) * ((1 / 10) * float(ast.literal_eval(skins[i])[3]))
                prob = float(ast.literal_eval(skins[i])[2][0]) * ((9/10)*float(ast.literal_eval(skins[i])[3]))
                probabilities.append([case,stat_trak_prob+prob])
    new_list = []
    case_prices = open('current/cases.txt','r')
    dic = '{'
    for case_price_line in case_prices.readlines():
        case_price_line = case_price_line.split(':::')
        dic = dic + f'"{case_price_line[0]}":"{case_price_line[1]}",'
    case_price_dic = ast.literal_eval((dic+'}').replace(',}','}'))
    for case in cases:
        addition=0
        for pro in probabilities:
            if pro[0]==case:
                addition=addition+pro[1]

        new_list.append([case,addition-1.89-float(case_price_dic[case])])
    print(new_list)
    #print(ast.literal_eval(inp_file.readlines().replace('\n','')))
    inp_file.close()
    out_file.close()

if __name__ == '__main__':
    start_time = time.time()
    from Prices import price_grabber
    avg_revenue_per_case()
    print(f'Steam Case Calc took - {(time.time()-start_time)/60} Mins')