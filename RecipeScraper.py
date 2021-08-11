from os import link
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import datetime
from bs4.element import PageElement, ResultSet, Tag
from dateutil.relativedelta import relativedelta
from urllib.error import HTTPError
import logging


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

def setup_logging():
    logging.basicConfig(filename="recipescraper.log",
                        encoding="utf-8", level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')


def close_logging():
    logging.info('Finished')


def get_recipe_urls_from_archive_page(archiveurl: str) -> list:
    url_list = []
    try:
        soup = get_parsed_html_from_url(archiveurl)
        article_elements = get_article_elements_from_page(soup)
        url_list.extend(
            get_article_urls_from_article_elements(article_elements))

        return url_list
    except HTTPError:
        return url_list


def get_article_elements_from_page(soup: BeautifulSoup) -> ResultSet:
    return soup.find_all("article")


def get_article_urls_from_article_elements(article_elements: ResultSet) -> list:
    url_list = []
    article_element: PageElement
    for article_element in article_elements:
        if isinstance(article_element, Tag):
            a_tag = article_element.find("a")
            if isinstance(a_tag, Tag):
                url = a_tag.get("href")
                url_list.append(url)

    return url_list


def get_archive_page_url_from_date(targetdate: datetime.date) -> str:
    paddedmonth = str(targetdate.month).zfill(2)
    return "https://www.budgetbytes.com/archive/{0}/{1}/".format(targetdate.year, paddedmonth)


def get_parsed_html_from_url(url: str) -> BeautifulSoup:
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

# print(get_recipe_urls_from_archive_page(
#     "https://www.budgetbytes.com/archive/2010/07"))


def scrape_full_recipe_URL_list():

    recipe_url_list = []

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
            currentpage = get_archive_page_url_from_date(currentdate)
            recipe_url_list.extend(
                get_recipe_urls_from_archive_page(currentpage))
            print("completed date: " + str(currentdate))

        recipefile.writelines(l + '\n' for l in recipe_url_list)


def get_recipe_urls(starting_line_index: int) -> list:
    with open("BudgetBytesRecipes.txt") as recipefile:
        recipe_urls = [line.strip() for line in recipefile]
        return recipe_urls[starting_line_index-1:]


class Recipe:
    def __init__(self, url="", name=None, ingredient_set=None, total_cost=None, serving_cost=None, servings=None, prep_time=None, cook_time=None, instruction_set=None, img_url=None):
        self.url = url
        self.name = name
        self.ingredient_set = ingredient_set
        self.total_cost = total_cost
        self.serving_cost = serving_cost
        self.servings = servings
        self.prep_time = prep_time
        self.cook_time = cook_time
        self.instruction_set = instruction_set
        self.img_url = img_url
        pass


class IngredientSet:
    def __init__(self, ingredient_list):
        self.ingredients = ingredient_list
        pass


class Ingredient:
    def __init__(self, name, amount, unit, price):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.price = price
        pass


class MeasurementUnit:
    def __init__(self, name):
        pass


class InstructionSet:
    def __init__(self, step_list):
        pass


class Step:
    def __init__(self):
        pass


def format_price(s: str) -> str:
    return s.replace("(", "").replace(")", "").replace("$", "")


def get_recipe_details_from_url(url: str) -> Recipe:
    try:
        logging.info(f"getting recipe details from url: {url}")
        soup = get_parsed_html_from_url(url)

        # TODO: extract method for each recipe attribute.
        # TODO: wrap each operation in a try block(?)
        # TODO: log events
        recipe_title = get_recipe_title(soup)

        # TODO: Parse the cost into real data
        cost_string = get_cost_string(soup)

        # TODO: Parse time strings into actual times
        total_time = get_total_time(soup)
        prep_time = get_prep_time(soup)
        cook_time = get_cook_time(soup)
        servings = get_servings(soup)
        servings_unit = get_servings_unit(soup)

        img_url = get_img_url(soup)

        ingredient_list = []

        ingredient_container = get_ingredient_container(soup)
        ingredient_elements = get_ingredient_elements(ingredient_container)

        for ingredient_element in ingredient_elements:
            current_ingredient = get_ingredient_from_element(
                ingredient_element)
            ingredient_list.append(current_ingredient)

        current_ingredient_set = IngredientSet(ingredient_list)

        # TODO: get instruction set data and put into recipe class

        current_recipe = Recipe(url, recipe_title, current_ingredient_set,
                                cost_string, cost_string, servings, prep_time, cook_time, None)

        return current_recipe

    except Exception:
        logging.exception(f"Error getting recipe details from url : {url}")
        raise


# TODO: unit test this
def get_ingredient_from_element(element: PageElement) -> Ingredient:
    current_amount = get_current_amount(element)
    current_unit = get_current_unit(element)
    if current_unit:
        current_unit = current_unit.string
    current_name = get_ingredient_name(element)
    current_price = get_ingredient_price(element)
    current_price = float(format_price(current_price))

    current_ingredient = Ingredient(
        current_name, current_amount, current_unit, current_price)

    return current_ingredient


def get_ingredient_price(i):
    return i.find(class_="wprm-recipe-ingredient-notes").string


def get_ingredient_name(i):
    return i.find(class_="wprm-recipe-ingredient-name").string


def get_current_unit(i):
    return i.find(class_="wprm-recipe-ingredient-unit")


def get_current_amount(i):
    return i.find(class_="wprm-recipe-ingredient-amount").string


def get_ingredient_elements(ingredient_container):
    return ingredient_container.find_all(class_="wprm-recipe-ingredient")


def get_ingredient_container(soup):
    return soup.find(class_="wprm-recipe-ingredients-container")


def get_img_url(soup):
    return soup.find(class_="wprm-recipe-image").img['data-src']


def get_servings_unit(soup):
    return soup.find(class_="wprm-recipe-servings-unit").string


def get_servings(soup):
    return soup.find(class_="wprm-recipe-servings").string


def get_cook_time(soup):
    return soup.find(class_="wprm-recipe-cook-time-container").get_text().strip()


def get_prep_time(soup):
    return soup.find(class_="wprm-recipe-prep-time-container").get_text().strip()


def get_total_time(soup):
    return soup.find(class_="wprm-recipe-total-time-container").get_text().strip()


def get_cost_string(soup):
    return soup.find(class_="wprm-recipe-recipe_cost").string


def get_recipe_title(soup):
    return soup.find(class_="wprm-recipe-name").string


# my_recipe = get_recipe_details_from_url(
#     "https://www.budgetbytes.com/beef-and-cauliflower-taco-skillet/")

pass


def Main():
    setup_logging()

    # my_recipes = []
    recipe_urls = []
    startline = 3
    recipe_urls = get_recipe_urls(startline)

    for i in range(10):
        current_recipe = get_recipe_details_from_url(recipe_urls[i])

    close_logging()


# Main()
