from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def get_parsed_html_from_url(url: str) -> BeautifulSoup:
    """Function: General scraping"""
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup
