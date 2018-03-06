import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from collections import Counter
from urllib.parse import urlparse


HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"}


def parse_verge_article(url):
    """get links in a theverge.com article.

    returns:
        counter: counter of links with corresponding hosts
    """
    # get the html of the article
    html = requests.get(url=url, headers=HEADERS)

    # parse into something we can use
    soup = bs(html.content, "html5lib")

    # get the html for the main story
    main = soup.find_all("div", class_="c-entry-content")[0]

    # get all the links
    links = main.find_all('a')

    # create a counter and add up all the hosts for the links we found
    cnt = Counter()
    for link in links:
        href = link.get('href')
        cnt[urlparse(href).netloc] += 1
    return soup, cnt


def parse_nytimes_article(url):
    """get links in a nytimes.com article.

    returns:
        counter: counter of links with corresponding hosts
    """
    html = requests.get(url=url, headers=HEADERS)
    soup = bs(html.content, "html5lib")
    main = soup.find(id="story")
    soup.find('div', class_="bottom-of-article").clear()
    paras = main.find_all('p')
    links = [link for content in paras for link in content.find_all('a')]
    cnt = Counter()
    for link in links:
        href = link.get('href')
        cnt[urlparse(href).netloc] += 1
    return soup, cnt
