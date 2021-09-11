import logging
import re

from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

import ScraperCommon
from models.Costs import Costs
from models.Ingredient import Ingredient
from models.IngredientSet import IngredientSet
from models.Recipe import Recipe


class RecipeDetailScraper():
    def get_recipe_details_from_url(self, url: str) -> Recipe:
        try:
            url = url.strip()
            logging.info(f"getting recipe details from url: {url}")
            soup = ScraperCommon.get_parsed_html_from_url(url)

            current_recipe = self.get_recipe_details_from_html(soup, url)
            logging.info(
                f"successfully retrieved recipe details from url: {url}")

            return current_recipe

        except ElementNotFound:
            logging.exception(
                f"Error getting recipe details from url : {url} (ElementNotFound)")
            raise
        except Exception:
            logging.exception(f"Error getting recipe details from url: {url}")
            raise

    def get_recipe_details_from_html(self, soup: BeautifulSoup, url: str = "") -> Recipe:
        # TODO: extract method for each recipe attribute.
        # TODO: wrap each operation in a try block(?)
        # TODO: log events
        recipe_title = self.get_recipe_title(soup)

        # TODO: Parse the cost into real data
        cost_data = self.get_cost_data(soup)

        # TODO: Parse time strings into actual times
        # total_time = get_total_time(soup)
        try:
            prep_time = self.get_prep_time(soup)
        except ElementNotFound:
            # means there is no prep time
            prep_time = 0
        try:
            cook_time = self.get_cook_time(soup)
        except ElementNotFound:
            raise
        servings = self.get_servings(soup)
        # servings_unit = get_servings_unit(soup)

        img_url = self.get_img_url(soup)

        # ingredient_elements = self.get_ingredient_elements(soup)
        current_ingredient_set = self.get_ingredient_set(soup)

        # TODO: get instruction set data and put into recipe class

        current_recipe = Recipe(url, recipe_title, current_ingredient_set,
                                cost_data.recipe_cost, cost_data.serving_cost, servings, prep_time, cook_time, None, img_url)
        return current_recipe

    def get_cost_data(self, soup: BeautifulSoup) -> Costs:
        recipe_cost = None
        serving_cost = None
        try:
            cost_string = str(self.get_cost_string(soup))
            recipe_cost = self.get_recipe_cost_from_cost_string(cost_string)
            try:
                serving_cost = self.get_serving_cost_from_cost_string(
                    cost_string)
            except ElementNotFound:
                # means the recipe_cost is the same as the serving cost
                serving_cost = recipe_cost

        except ElementNotFound:
            # old format
            recipe_cost = self.get_old_format_recipe_cost(soup)
            serving_cost = self.get_old_format_serving_cost(soup)

        costs = Costs(serving_cost, recipe_cost)
        return costs

    def get_old_format_recipe_cost(self, soup):
        result = str(soup.find(string=re.compile("Total Recipe cost")))
        cost = result.replace("Total Recipe cost: $", "").strip()
        return cost

    def get_old_format_serving_cost(self, soup):
        result = str(soup.find(string=re.compile("Cost per serving")))
        cost = result.replace("Cost per serving: $", "").strip()
        return cost

    def get_ingredient_set_from_elements(self, ingredient_elements):
        ingredient_list = []

        for ingredient_element in ingredient_elements:
            current_ingredient = self.get_ingredient_from_element(
                ingredient_element)
            ingredient_list.append(current_ingredient)

        current_ingredient_set = IngredientSet(ingredient_list)
        return current_ingredient_set

    def get_ingredient_set(self, soup):
        ingredient_elements = self.get_ingredient_elements(soup)
        return self.get_ingredient_set_from_elements(ingredient_elements)

    # TODO: unit test this

    # TODO: add support for ingredient sections?

    def get_ingredient_from_element(self, element: PageElement) -> Ingredient:
        current_amount = self.get_current_amount(element)
        current_unit = self.get_current_unit(element)
        current_name = self.get_ingredient_name(element)
        current_price = self.get_ingredient_price(element)
        current_price = float(self.format_price(current_price))

        current_ingredient = Ingredient(
            current_name, current_amount, current_unit, current_price)

        return current_ingredient

    def get_recipe_urls(self, starting_line_index: int) -> list:
        with open("BudgetBytesRecipes.txt") as recipefile:
            recipe_urls = [line.strip() for line in recipefile]
            return recipe_urls[starting_line_index-1:]

    def format_price(self, s: str) -> str:
        return s.replace("(", "").replace(")", "").replace("$", "").replace("*", "")

    def get_ingredient_price(self, element):
        result = ""
        if isinstance(element, Tag):
            price_element = element.find(class_="wprm-recipe-ingredient-notes")
            if price_element is not None:
                result = price_element.string
        if result is not None:
            return result
        else:
            return ""

    def get_recipe_cost_from_cost_string(self, cost_string: str) -> float:
        recipe_word_index = cost_string.index('recipe')
        recipe_cost_string = cost_string[:recipe_word_index]
        recipe_cost_string = recipe_cost_string.replace("$", "")
        recipe_cost_string = recipe_cost_string.strip()
        recipe_cost = float(recipe_cost_string)
        return recipe_cost

    def get_serving_cost_from_cost_string(self, cost_string: str) -> float:
        try:
            slash_character_index = cost_string.index("/")
            serving_word_index = cost_string.index('serving')
            serving_cost_string = cost_string[slash_character_index:serving_word_index]
            serving_cost_string = serving_cost_string.replace("$", "")
            serving_cost_string = serving_cost_string.replace("/", "")
            serving_cost_string = serving_cost_string.strip()
            serving_cost = float(serving_cost_string)
            return serving_cost
        except:
            raise ElementNotFound("Could not get serving cost")

    def get_ingredient_name(self, element):
        result = ""
        if isinstance(element, Tag):
            ingredient_element = element.find(
                class_="wprm-recipe-ingredient-name")
            if ingredient_element is not None:
                if ingredient_element.string is not None:
                    result = ingredient_element.string.strip()
        return result

    def get_current_unit(self, element) -> str:
        result = ""
        if isinstance(element, Tag):
            unit_element = element.find(class_="wprm-recipe-ingredient-unit")
            if unit_element is not None:
                if unit_element.string is not None:
                    result = unit_element.string
        return result

    def get_current_amount(self, element):
        amount = ""
        if isinstance(element, Tag):
            ingredient_tag = element.find(
                class_="wprm-recipe-ingredient-amount")
            if ingredient_tag is not None:
                amount = ingredient_tag.string
        if amount is not None:
            return amount
        else:
            return ""

    def get_ingredient_elements(self, soup):
        result = None
        ingredient_container = self.get_ingredient_container(soup)
        if isinstance(ingredient_container, Tag):
            result = ingredient_container.find_all(
                class_="wprm-recipe-ingredient")
        return result

    def get_ingredient_container(self, soup):
        return soup.find(class_="wprm-recipe-ingredients-container")

    def get_img_url(self, soup):
        return soup.find(class_="wprm-recipe-image").img['data-src']

    def get_servings_unit(self, soup):
        return soup.find(class_="wprm-recipe-servings-unit").string

    def get_servings(self, soup):
        return int(soup.find(class_="wprm-recipe-servings").string)

    def get_cook_time(self, soup):
        result_time = 0
        try:
            cook_time_string = soup.find(
                class_="wprm-recipe-cook-time-container").get_text().strip()
            # cook_time_string = cook_time_string.replace("Cook Time:", "")
            hours_component_index = cook_time_string.find("hr")

            if hours_component_index != -1:
                hours_component = cook_time_string[:hours_component_index]
                # hours_component = hours_component.replace(
                #     "hr", "").replace("s", "")
                # hours_component = hours_component.strip()

                hours_component = ''.join(
                    c for c in hours_component if c.isdigit())
                result_time += int(hours_component) * 60
                minutes_component = cook_time_string[hours_component_index:]
                # minutes_component = minutes_component.replace(
                # "mins", "").strip()

                minutes_component = ''.join(
                    c for c in minutes_component if c.isdigit())
                result_time += int(minutes_component)

            else:
                # cook_time_string = cook_time_string.replace("mins", "")
                # cook_time_string = cook_time_string.strip()

                cook_time_string = ''.join(
                    c for c in cook_time_string if c.isdigit())
                result_time += int(cook_time_string)

            return result_time
        except:
            raise ElementNotFound("Could not get Cook time")

    def get_prep_time(self, soup):
        try:
            prep_time_string = soup.find(
                class_="wprm-recipe-prep-time-container").get_text().strip()
            prep_time = prep_time_string.replace("Prep Time:", "")
            prep_time = prep_time.replace("mins", "")
            prep_time = prep_time.strip()
            return int(prep_time)
        except:
            raise ElementNotFound("Could not get Prep time")

    def get_total_time(self, soup):
        return soup.find(class_="wprm-recipe-total-time-container").get_text().strip()

    def get_cost_string(self, soup):
        result = soup.find(class_="wprm-recipe-recipe_cost")
        if result:
            return result.string
        else:
            raise ElementNotFound("Could not find cost string")

    def get_recipe_title(self, soup):
        result = soup.find(class_="wprm-recipe-name")
        if result:
            return result.string
        else:
            # old format
            old_format_result = soup.find(class_="post-title").h1
            if old_format_result:
                return old_format_result
            else:
                raise ElementNotFound("Could not find recipe title")


class ElementNotFound(Exception):
    """Raised when an element can't be found in the html"""
    pass


class CouldNotScrapeRecipe(Exception):
    pass
