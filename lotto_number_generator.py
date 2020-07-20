from bs4 import BeautifulSoup
import requests

import random

LOTTO_URL = 'https://games.lotto.is/result/lotto-statistics'
VIKING_LOTTO_URL = 'https://games.lotto.is/result/vikinga-statistics'

NUMBERS_PER_JOKER_ROW = 5

def generate_row(a_dict, num_per_row, repeating):
    row = []
    keys = list(a_dict.keys())
    values  = list(a_dict.values())

    for _ in range(num_per_row):
        number = random.choices(keys, values)[0]
        if not repeating:
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

def get_url():
    choice = get_user_choice()

    url = ""

    if choice.startswith('l'):
        url = LOTTO_URL
    elif choice.startswith('v'):
        url = VIKING_LOTTO_URL
    
    return url

def get_numbers_per_lotto_row(url):
    numbers_per_lotto_row = 5

    if url == LOTTO_URL:
        numbers_per_lotto_row = 5
    elif url == VIKING_LOTTO_URL:
        numbers_per_lotto_row = 6

    return numbers_per_lotto_row

def get_soup(url):   
    html = requests.get(url).text
    return BeautifulSoup(html, 'html.parser')

def get_dict(soup, is_lotto_row):
    a_dict = dict()

    if is_lotto_row:
        data = soup.find('tbody').find_all('td')
    else:
        data = soup.find_all('tbody')[1].find_all('td')

    fill_dict(a_dict, data)

    return a_dict

def get_viking_dict(lotto_dict, url):
    if url != VIKING_LOTTO_URL:
        return None

    viking_dict = dict()
    for i in range(1,9):
        viking_dict[i] = lotto_dict[i]

    return viking_dict

def get_rows(row_count, numbers_per_row, a_dict, repeating):
    rows = []
    for _ in range(row_count):
        rows.append(generate_row(a_dict, numbers_per_row, repeating))

    return rows

def write_rows_to_file(filename, rows, viking_dict=None):
    with open(filename, 'w') as f:
        for row in rows:
            row_str = ' '.join(row)
            f.write(row_str)
            print(row_str, end=" ")
            if viking_dict != None:
                viking_number = generate_row(viking_dict, 1, True)[0]
                f.write(" " + viking_number)
                print(" " + viking_number, end="")
            f.write('\n')
            print()

def main():
    url = get_url()
    numbers_per_lotto_row = get_numbers_per_lotto_row(url)
    soup = get_soup(url)
    
    lotto_dict = get_dict(soup, False)
    joker_dict = get_dict(soup, True)
    viking_dict = get_viking_dict(lotto_dict, url)
    
    lotto_row_count = int(input('How many lotto rows do you want: '))
    joker_row_count = int(input('How many joker rows do you want: '))

    lotto_rows = get_rows(lotto_row_count, numbers_per_lotto_row, lotto_dict, False)
    joker_rows = get_rows(joker_row_count, NUMBERS_PER_JOKER_ROW, joker_dict, True)

    print("Here are your lotto rows:")
    write_rows_to_file("lotto.txt", lotto_rows,viking_dict)

    print()
    
    print("Here are your joker rows:")
    write_rows_to_file("joker.txt", joker_rows)

main()