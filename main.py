import requests, re
from pprint import pprint as pp
from bs4 import BeautifulSoup as bs

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/all/'


def get_articles(keywords, url):
    resp_outer = requests.get(url)
    soup_outer = bs(resp_outer.text, 'html.parser')

    articles = soup_outer.find_all('article', class_='post_preview')
    for article in articles:
        link = article.find('a', class_='post__title_link')
        link_url = link.attrs.get('href')
        resp_inner = requests.get(link_url)
        soup_inner = bs(resp_inner.text, 'html.parser')

        inner_text_html = bs(soup_inner.find('div', class_="post__text").text, 'html.parser').text
        words = [word.group() for word in re.finditer(r"[a-zа-я]{2,}", inner_text_html.lower())]
        for word in words:
            if any([keyword in word for keyword in keywords]):
                print(f'Дата: {article.find("span", class_="post__time").text} - {link.text} - {link_url}')
                break

    active_page = soup_outer.find('span', class_='toggle-menu__item-link_active')
    try:
        next_page = active_page.parent.findNext('li').find('a').text
    except AttributeError:
        print('ALL DONE!!!')
    else:
        url = URL + 'page' + next_page
        get_articles(keywords, url)


if __name__ == '__main__':
    get_articles(KEYWORDS, URL)
