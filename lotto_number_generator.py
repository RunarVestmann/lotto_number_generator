from bs4 import BeautifulSoup
import requests as r

import random

NUMBERS_PER_LOTTO_ROW = 6
NUMBERS_PER_JOKER_ROW = 5

def generate_row(a_dict, num_per_row):
    row = []
    keys = list(a_dict.keys())
    values  = list(a_dict.values())

    for _ in range(num_per_row):
        number = random.choices(keys, values)[0]
        values.remove(a_dict[number])
        keys.remove(number) 
        row.append(str(number))

    return row

def get_user_choice():
    print('(L)otto\t(V)iking lotto')
    choice = input('Choice: ').lower()
    while not choice.startswith('l') and not choice.startswith('v'):
        print("Please enter 'l' or 'v'")
        print('(L)otto\t(V)iking')
        choice = input('Choice: ').lower()
    return choice

def fill_dict(a_dict, data):
    for i in range(0, len(data)-2, 2):
        a_dict[int(data[i].text.strip())] = int(data[i+1].text.strip())

lotto_url = 'https://games.lotto.is/result/lotto-statistics'
viking_lotto_url = 'https://games.lotto.is/result/vikinga-statistics'

url = ''
choice = get_user_choice()
if choice.startswith('l'):
    url = lotto_url
    NUMBERS_PER_LOTTO_ROW = 5
elif choice.startswith('v'):
    url = viking_lotto_url
    NUMBERS_PER_LOTTO_ROW = 6

html = r.get(url).text

soup = BeautifulSoup(html, 'html.parser')

lotto_dict = dict()
lotto_data = soup.find('tbody').find_all('td')
fill_dict(lotto_dict, lotto_data)

joker_data = soup.find_all('tbody')[1].find_all('td')
joker_dict = dict()
fill_dict(joker_dict, joker_data)

lotto_row_count = int(input('How many lotto rows do you want: '))
joker_row_count = int(input('How many joker rows do you want: '))

lotto_rows = []
for _ in range(lotto_row_count):
    lotto_rows.append(generate_row(lotto_dict, NUMBERS_PER_LOTTO_ROW))

joker_rows = []
for _ in range(joker_row_count):
    joker_rows.append(generate_row(joker_dict, NUMBERS_PER_JOKER_ROW))

with open('lotto.txt', 'a+') as l:
    for row in lotto_rows:
        l.write(' '.join(row))
        l.write('\n')

with open('joker.txt', 'a+') as j:
    for row in joker_rows:
        j.write(' '.join(row))
        j.write('\n')
