import string

import requests
import os
from bs4 import BeautifulSoup


def input_processing():
    pages = int(input())
    article_type = input()
    return pages, article_type


def dir_maker(page):
    os.getcwd()
    os.mkdir(f'Page_{str(page)}')
    os.chdir(f'{os.getcwd()}\\Page_{str(page)}')


def url_processing(curr_page):
    dir_maker(curr_page)
    url_input = f'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page={curr_page}'

    r = requests.get(url_input, headers={'Accept-Language': 'en-US,en;q=0.5'})
    s_code = r.status_code
    r_content = r.content

    if s_code > 300:
        print(f'\nThe URL returned {s_code}!')
        return

    return r_content


def page_save(page_content, article_name):
    try:
        with open(f'{article_name}.txt', 'w', encoding='utf-8') as f:
            f.write(page_content)
    except Exception as e:
        print(f'\nThe URL returned {Exception}')


def name_formatting(article_name):
    word_list = article_name.split()
    new_sentence = list()
    for number, name in enumerate(word_list):
        new_word = list()
        for char in name:
            if char not in string.punctuation:
                new_word.append(char)
        new_sentence.append(''.join(new_word))
    return ' '.join(new_sentence).replace(' ', '_')


def second_soup(joined_url):
    r = requests.get(joined_url, headers={'Accept-Language': 'en-US,en;q=0.5'})

    if r.status_code > 300:
        print(f'\nThe URL returned {r.status_code}!')
        return

    s_soup = BeautifulSoup(r.content, 'html.parser')
    page_content = s_soup.find('div', {'class': 'c-article-body u-clearfix'}).text
    return page_content


def processed_soup(req_content, content_type):
    base_url = 'https://www.nature.com'
    try:
        soup = BeautifulSoup(req_content, 'html.parser')
        articles = soup.find_all('span', {'class': 'c-meta__type'}, text=f'{content_type}')
        for article in articles:
            parent = article.find_parent('article').find('a', {'data-track-action': 'view article'})
            link = parent.get('href')
            sub_url = f'{base_url}{link}'
            p_content = second_soup(sub_url)
            formatted_article_name = name_formatting(parent.text)
            try:
                page_save(p_content, formatted_article_name)
            except Exception as e:
                pass
    except AttributeError:
        print('Invalid movie page!')
    except Exception as e:
        raise e
    os.chdir('..')


pages, article_type = input_processing()
for i in range(1, pages+1):
    content = url_processing(i)
    processed_soup(content, article_type)
