from Models.Recipe import Recipe
from Models.Ingredient import Ingredient
from Models.IngredientSet import IngredientSet
import logging
import ScraperCommon
from bs4.element import PageElement, ResultSet, Tag


class RecipeDetailScraper():
    def get_recipe_details_from_url(self, url: str) -> Recipe:
        """Function: Scrape Recipe Details"""
        try:
            logging.info(f"getting recipe details from url: {url}")
            soup = ScraperCommon.get_parsed_html_from_url(url)

            # TODO: extract method for each recipe attribute.
            # TODO: wrap each operation in a try block(?)
            # TODO: log events
            recipe_title = get_recipe_title(soup)

            # TODO: Parse the cost into real data
            cost_string = get_cost_string(soup)

            # TODO: Parse time strings into actual times
            # total_time = get_total_time(soup)
            prep_time = get_prep_time(soup)
            cook_time = get_cook_time(soup)
            servings = get_servings(soup)
            # servings_unit = get_servings_unit(soup)

            # img_url = get_img_url(soup)

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
    """Function: Scrape Recipe Details"""
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


def get_recipe_urls(self, starting_line_index: int) -> list:
    """Function: Scrape Recipe Details"""
    with open("BudgetBytesRecipes.txt") as recipefile:
        recipe_urls = [line.strip() for line in recipefile]
        return recipe_urls[starting_line_index-1:]


def format_price(s: str) -> str:
    """Function: Scrape Recipe Details"""
    return s.replace("(", "").replace(")", "").replace("$", "")


def get_ingredient_price(i):
    """Function: Scrape Recipe Details"""
    return i.find(class_="wprm-recipe-ingredient-notes").string


def get_ingredient_name(i):
    """Function: Scrape Recipe Details"""
    return i.find(class_="wprm-recipe-ingredient-name").string


def get_current_unit(i):
    """Function: Scrape Recipe Details"""
    return i.find(class_="wprm-recipe-ingredient-unit")


def get_current_amount(i):
    """Function: Scrape Recipe Details"""
    return i.find(class_="wprm-recipe-ingredient-amount").string


def get_ingredient_elements(ingredient_container):
    """Function: Scrape Recipe Details"""
    return ingredient_container.find_all(class_="wprm-recipe-ingredient")


def get_ingredient_container(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-ingredients-container")


def get_img_url(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-image").img['data-src']


def get_servings_unit(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-servings-unit").string


def get_servings(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-servings").string


def get_cook_time(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-cook-time-container").get_text().strip()


def get_prep_time(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-prep-time-container").get_text().strip()


def get_total_time(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-total-time-container").get_text().strip()


def get_cost_string(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-recipe_cost").string


def get_recipe_title(soup):
    """Function: Scrape Recipe Details"""
    return soup.find(class_="wprm-recipe-name").string
