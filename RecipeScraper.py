from os import link
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import datetime
from dateutil.relativedelta import relativedelta
from urllib.error import HTTPError


# url = "https://www.budgetbytes.com/archive/2010/07"
# req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
# page = urlopen(req)
# html = page.read().decode("utf-8")
# soup = BeautifulSoup(html, "html.parser")

# print(soup.get_text())

# image1, image2 = soup.find_all("img")

# print(image1["src"])

# articlelist = soup.find_all("article")
# linklist = []
# for a in articlelist:
#     # print(a)
#     linklist.append(a.find("a"))

# for l in linklist:
#     print(l.get("href"))

recipe_url_list = []


def get_recipe_urls_from_archive_page(archiveurl):
    linklist = []
    try:
        req = Request(archiveurl, headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req)
        html = page.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        articleElements = soup.find_all("article")

        for a in articleElements:
            linklist.append(a.find("a").get("href"))

        return linklist
    except HTTPError:
        return linklist


def get_archive_page_url(targetdate):
    paddedmonth = str(targetdate.month).zfill(2)
    return "https://budgetbytes.com/archive/{0}/{1}/".format(targetdate.year, paddedmonth)


# print(get_recipe_urls_from_archive_page(
#     "https://www.budgetbytes.com/archive/2010/07"))


archive_start_date = datetime.date(2009, 5, 1)
archive_end_date = datetime.date(
    datetime.date.today().year, datetime.date.today().month, 1)


with open("BudgetBytesRecipes.txt", 'w') as recipefile:
    for i in range(0, 1000):
        currentdate = datetime.date(
            archive_start_date.year, archive_start_date.month, archive_start_date.day)
        currentdate = currentdate + relativedelta(months=+i)
        if currentdate == archive_end_date:
            break
        # print(currentdate)
        # print(get_archive_page_url(currentdate))
        currentpage = get_archive_page_url(currentdate)
        recipe_url_list.extend(get_recipe_urls_from_archive_page(currentpage))
        print("completed date: " + str(currentdate))

    recipefile.writelines(l + '\n' for l in recipe_url_list)


class Recipe:
    def __init__(self, url, name, ingredient_set):
        pass


class IngredientSet:
    def __init__(self, ingredient_list):
        pass


class Ingredient:
    def __init__(self, name, amount, unit):
        pass


class MeasurementUnit:
    def __init__(self, name):
        pass
