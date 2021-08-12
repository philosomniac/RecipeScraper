from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


TestSoupFilePath = "TestSoupFiles\\"


def get_parsed_html_from_url(url: str) -> BeautifulSoup:
    """Function: General scraping"""
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


def save_soup_to_file(url: str, file_name: str):
    soup = get_parsed_html_from_url(url)
    file_path = TestSoupFilePath + file_name
    with open(file_path, "w", encoding='utf-8') as output_file:
        output_file.write(str(soup))


def get_soup_from_test_file(file_name: str) -> BeautifulSoup:
    file_path = TestSoupFilePath + file_name
    with open(file_path, encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    return soup
