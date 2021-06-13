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


def get_recipe_urls_from_archive_page(archiveurl):
    linklist = []
    try:
        # req = Request(archiveurl, headers={'User-Agent': 'Mozilla/5.0'})
        # page = urlopen(req)
        # html = page.read().decode("utf-8")
        # soup = BeautifulSoup(html, "html.parser")
        soup = get_parsed_html_from_url(archiveurl)
        articleElements = soup.find_all("article")

        for a in articleElements:
            linklist.append(a.find("a").get("href"))

        return linklist
    except HTTPError:
        return linklist


def get_archive_page_url(targetdate):
    paddedmonth = str(targetdate.month).zfill(2)
    return "https://budgetbytes.com/archive/{0}/{1}/".format(targetdate.year, paddedmonth)


def get_parsed_html_from_url(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

# print(get_recipe_urls_from_archive_page(
#     "https://www.budgetbytes.com/archive/2010/07"))


def get_full_recipe_URL_list():

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
            # print(currentdate)
            # print(get_archive_page_url(currentdate))
            currentpage = get_archive_page_url(currentdate)
            recipe_url_list.extend(
                get_recipe_urls_from_archive_page(currentpage))
            print("completed date: " + str(currentdate))

        recipefile.writelines(l + '\n' for l in recipe_url_list)


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


def format_price(s):
    return s.replace("(", "").replace(")", "").replace("$", "")


def get_recipe_details_from_url(url):
    try:
        soup = get_parsed_html_from_url(url)

        # TODO: extract method for each recipe attribute.
        # TODO: wrap each operation in a try block(?)
        # TODO: log events
        recipe_title = soup.find(class_="wprm-recipe-name").string

        # TODO: Parse the cost into real data
        cost_string = soup.find(class_="wprm-recipe-recipe_cost").string

        # TODO: Parse time strings into actual times
        total_time = soup.find(
            class_="wprm-recipe-total-time-container").get_text().strip()
        prep_time = soup.find(
            class_="wprm-recipe-prep-time-container").get_text().strip()
        cook_time = soup.find(
            class_="wprm-recipe-cook-time-container").get_text().strip()
        servings = soup.find(class_="wprm-recipe-servings").string
        servings_unit = soup.find(class_="wprm-recipe-servings-unit").string

        img_url = soup.find(class_="wprm-recipe-image").img['data-src']

        ingredient_list = []

        ingredient_container = soup.find(
            class_="wprm-recipe-ingredients-container")
        ingredient_elements = ingredient_container.find_all(
            class_="wprm-recipe-ingredient")

        for i in ingredient_elements:
            current_amount = i.find(
                class_="wprm-recipe-ingredient-amount").string
            current_unit = i.find(class_="wprm-recipe-ingredient-unit")
            if current_unit:
                current_unit = current_unit.string
            current_name = i.find(class_="wprm-recipe-ingredient-name").string
            current_price = i.find(
                class_="wprm-recipe-ingredient-notes").string
            current_price = float(format_price(current_price))
            current_ingredient = Ingredient(
                current_name, current_amount, current_unit, current_price)
            ingredient_list.append(current_ingredient)

            pass

        current_ingredient_set = IngredientSet(ingredient_list)

        # TODO: get instruction set data and put into recipe class

        current_recipe = Recipe(url, recipe_title, current_ingredient_set,
                                cost_string, cost_string, servings, prep_time, cook_time, None)

        return current_recipe
        pass

    except:
        raise


my_recipe = get_recipe_details_from_url(
    "https://www.budgetbytes.com/beef-and-cauliflower-taco-skillet/")

pass
