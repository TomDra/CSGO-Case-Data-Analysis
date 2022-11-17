import requests
import ast
import time
import datetime
import shutil
import os

rarity = {
    '4b69ff': 'Mil-spec',
    '8847ff': 'Restricted',
    'd32ce6': 'Classified',
    'eb4b4b': 'Covert'
}
all_wears = ['Mil-spec', 'Restricted', 'Classified', 'Covert']
probabilites = {
    'Mil-spec': 79.92,
    'Restricted': 15.98,
    'Classified': 3.2,
    'Covert': 0.64,
    'Rare-Item': 0.26
}


def add_date(file):
    file = file.replace('.txt', '')
    date_time = str(datetime.datetime.now())
    date = date_time.split(' ')[0]
    time = '-'.join(date_time.split(' ')[1].split(':')[:2])
    new_file = f'{file}¦{date}¦{time}.txt'
    return new_file


def cases(out):
    """ Creates a list of all cases, their price and every skin inside the case and add it to the file given (out) """
    print('Starting Case Compiler (Approx 9 mins):')
    time_ = time.time()
    cases = []
    r = requests.get('https://csgostash.com/containers/skin-cases')
    f = open(out, 'w+')
    clist = str(r.content).replace("b'", '').split('<div class="col-lg-4 col-md-6 col-widen text-center">')
    for c in clist:
        if '<div class="well result-box nomargin">' in c:
            price = c.split('<p class="nomargin">')[1].split('</p>')[0].replace('\\xc2\\xa3', '').replace('$', '')
            case_name = c.split('<h4>')[1].split('</h4>')[0].replace('amp;', '')
            cases.append(ast.literal_eval(f'["{case_name}","{price}"]'))
    print(cases)

    for case in cases:
        start_time = time.time()
        items = []
        try:
            items_web = requests.get(('https://steamcommunity.com/market/listings/730/' + case[0]).replace(' ', '%20'))
            if not items_web.ok:
                print('             Too Many Requests!')
            dic = (str(items_web.content).split('var g_rgAssets')[1].split(
                '{"type":"html","value":"Contains one of the following:"}')[1].split(f',"name":"{case[0]}"')[0].split(
                ',"tradable"')[0])
            dic = '[' + dic[1:len(dic)]
            dic = ast.literal_eval(dic)  # Creates a list of all the items in the case
            dic = dic[0:len(dic) - 3]
            for i in range(0, len(dic)):
                gun = (dic[i]['value']).replace('\\u2665', '')
                rareness = rarity[dic[i]['color']]
                items.append([gun, rareness])  # Adds each run and its rarity to the list
            print(f'[Case_Compiler] ~ {case[0]}, {items_web}, took {time.time() - start_time} seconds')
        except IndexError as e:
            print('Ignoring ' + case[0], e)
        items_web.close()
        time.sleep(20)
        f.write(case[0] + ':::' + case[1] + ':::' + str(items) + '\n')
    print(f'Case Compiler Took - {(time.time() - time_) / 60} mins')
    f.close()


def csgo_stash_ids(file):
    print('Starting the CsgoStash ID compiler (Approx 19 minutes):')
    i = 0
    names = []
    end = []
    for temp in range(0, 30):
        end.append('')
    csgo_stash_data = open(file, 'w+')
    start_time = time.time()
    prev_time = time.time()
    while True:
        website = requests.get(f'https://csgostash.com/skin/{i}/')
        name = str(website.url.replace(f'https://csgostash.com/skin/{i}/', '')).replace('%E2%99%A5', '').replace(
            '\\u2665', '').replace('\xe2\x99\xa5', '')  # .encode('utf-8')
        names.append(name)
        csgo_stash_data.write(f'{name}<{i}>{name}:::')
        if names[len(names) - 30:] == end:
            csgo_stash_data.close()
            print(f'Stopped at - {i - 30}, total time - {(time.time() - start_time) / 60} minutes')
            break
        if i % 50 == 0:
            print(f'[Csgo_Stash_Ids] ~ Found {i} Ids, took {time.time() - prev_time} seconds')
            prev_time = time.time()
        i = i + 1


def extract(html):
    html = html.split('\n')
    temp = 2
    if 'StatTrak' in html[1] or 'StatTrak' in html[2]:
        stattrak = True
        temp = 3
    else:
        stattrak = False
    wear = html[temp].replace('<span class="pull-left">', '').replace('</span>', '').replace(
        '<span class="pull-left price-details-st">', '')
    price = html[temp + 1].replace('<span class="pull-right">', '').replace('</span>', '').replace(
        '<span class="pull-left">', '').replace('£', '').replace('$', '')
    return [stattrak, wear, price]


def csgostash_price(ids, skin):
    remove = ['(', ')', "'", '.', '<', '>']
    prices = []
    converted_skin = skin.replace(' | ', '-').replace(' ', '-').replace('\\u9f8d\\u738b', '%E9%BE%8D%E7%8E%8B').replace(
        '_', '-')
    for rem in remove:
        converted_skin = converted_skin.replace(rem, '')
    id_file = open(ids, 'r', encoding='utf-8')
    try:
        id_contents = (id_file.read().split(converted_skin))[1]
        s_id = id_contents.replace('<', '').replace('>', '')
        website = requests.get((f'https://csgostash.com/skin/{s_id}'))
        r = website.text.split('<div class="btn-group-sm btn-group-justified">')
        if '<span class="pull-left price-details-st">StatTrak</span>' in r[2].split('\n'):
            for i in range(2, 2 + 10):
                values = r[i].split('</a>')[0]
                prices.append(extract(values))
        else:
            for i in range(2, 2 + 5):
                values = r[i].split('</a>')[0]
                prices.append(extract(values))
        nst_prices = []
        st_prices = []
        nst_total = 0
        st_total = 0
        for i in range(0, len(prices)):
            if not prices[i][0]:
                if prices[i][2].replace(' ', '') != 'NotPossible':
                    if prices[i][2].replace(' ', '') != 'NoRecentPrice':
                        nst_prices.append(float(prices[i][2].replace(',', '')))
            else:
                if prices[i][2].replace(' ', '') != 'NotPossible':
                    if prices[i][2].replace(' ', '') != 'NoRecentPrice':
                        st_prices.append(float(prices[i][2].replace(',', '')))
        for nst_price in nst_prices:
            nst_total = nst_total + nst_price
        for st_price in st_prices:
            st_total = st_total + st_price
        if st_total != 0:
            avg_stattrak = str(st_total / (len(st_prices)))
        else:
            avg_stattrak = 'NO PRICE'
        if nst_total != 0:
            avg_nonstattrak = str(nst_total / (len(nst_prices)))
        else:
            avg_nonstattrak = 'NO PRICE'
        avg_prices = [avg_nonstattrak, avg_stattrak]
    except KeyError as e:
        print(converted_skin, e)
    id_file.close()
    return avg_prices


def skin_prices(ids, inp, out):
    total_time = time.time()
    print('Getting all case skin prices (Approx 7 mins):')
    skins = []
    ifile = open(str(inp), 'r')
    ofile = open(str(out), 'w+')
    ilines = ifile.readlines()
    for iline in ilines:
        start_time = time.time()
        amount = '{'
        cases = iline.split(':::')
        case = cases[0]
        for all_wear in all_wears:
            count = iline.count(all_wear)
            amount = f"{amount} '{all_wear}':{count},"
        amount = ast.literal_eval((amount + '}').replace(',}', '}'))
        for skin_list in ast.literal_eval(cases[2]):
            wear = skin_list[1]
            skin = skin_list[0]
            probability = probabilites[wear] / amount[wear] / 100
            price = csgostash_price(ids, skin)
            skins.append([case, skin, price, probability])
        print(f'Searched - {case}, took {time.time() - start_time} Seconds')
    for skin in skins:
        ofile.write(str(skin) + '\n')
    ofile.close()
    print(f'Compleated searching skin prices, took - {(time.time() - total_time) / 60} mins')


def archive(files):
    if os.path.exists(f'current/'):
        shutil.rmtree('current')
        os.makedirs('current')
    else:
        os.makedirs('current')
    if not os.path.exists('archive'):
        os.makedirs('archive')

    for file in files:
        shutil.copy(f'{file}', f'archive/{add_date(file)}')
        os.rename(str(file), f'current/{file}')


def item_case_search(files):
    import multiprocessing
    case_file = files[0]
    price_file = files[1]
    stash_ids = files[2]
    processes = []
    p = multiprocessing.Process(target=cases, args=[case_file])
    p.start()
    processes.append(p)
    p = multiprocessing.Process(target=csgo_stash_ids, args=[stash_ids])
    p.start()
    processes.append(p)
    for p in processes:
        p.join()
    skin_prices(stash_ids, case_file, price_file)
    # if not os.path.exists(stash_ids):
    # csgo_stash_ids(stash_ids)
