from bs4 import BeautifulSoup
import os
import requests
import urllib.parse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
URL = 'https://magic.wizards.com/en/rules'
OUT = os.path.join(BASE_DIR, 'data', 'lib')


def get_html():
    # TODO: error handling
    response = requests.get(URL)
    html = response.text
    return html


def make_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select('a.cta[href$=".txt"]')
    if len(links) != 1:
        raise IndexError
    return links[0].attrs.get('href')


def write_rules_from_link(link, encoding='utf-8'):
    # encoding = response.encoding
    # TODO: error handling
    response = requests.get(link)
    content = response.content.decode(encoding)
    title = urllib.parse.unquote(link.split('/')[-1])
    with open(os.path.join(OUT, title), 'w', encoding=encoding) as f:
        f.write(content)


def main():
    html = get_html()
    link = make_soup(html)
    write_rules_from_link(link)

if __name__ == '__main__':
    main()
