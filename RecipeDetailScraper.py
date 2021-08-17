from Models.Recipe import Recipe
from Models.Ingredient import Ingredient
from Models.IngredientSet import IngredientSet
import logging
import ScraperCommon
from bs4.element import PageElement, ResultSet, Tag


class RecipeDetailScraper():
    def get_recipe_details_from_url(self, url: str) -> Recipe:
        try:
            logging.info(f"getting recipe details from url: {url}")
            soup = ScraperCommon.get_parsed_html_from_url(url)

            # TODO: extract method for each recipe attribute.
            # TODO: wrap each operation in a try block(?)
            # TODO: log events
            recipe_title = self.get_recipe_title(soup)

            # TODO: Parse the cost into real data
            cost_string = self.get_cost_string(soup)

            # TODO: Parse time strings into actual times
            # total_time = get_total_time(soup)
            prep_time = self.get_prep_time(soup)
            cook_time = self.get_cook_time(soup)
            servings = self.get_servings(soup)
            # servings_unit = get_servings_unit(soup)

            # img_url = get_img_url(soup)

            # ingredient_elements = self.get_ingredient_elements(soup)
            current_ingredient_set = self.get_ingredient_set(soup)

            # TODO: get instruction set data and put into recipe class

            current_recipe = Recipe(url, recipe_title, current_ingredient_set,
                                    cost_string, cost_string, servings, prep_time, cook_time, None)

            return current_recipe

        except Exception:
            logging.exception(f"Error getting recipe details from url : {url}")
            raise

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
        return s.replace("(", "").replace(")", "").replace("$", "")

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

    def get_ingredient_name(self, element):
        result = ""
        if isinstance(element, Tag):
            ingredient_element = element.find(
                class_="wprm-recipe-ingredient-name")
            if ingredient_element is not None:
                if ingredient_element.string is not None:
                    result = ingredient_element.string
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
        return soup.find(class_="wprm-recipe-servings").string

    def get_cook_time(self, soup):
        return soup.find(class_="wprm-recipe-cook-time-container").get_text().strip()

    def get_prep_time(self, soup):
        return soup.find(class_="wprm-recipe-prep-time-container").get_text().strip()

    def get_total_time(self, soup):
        return soup.find(class_="wprm-recipe-total-time-container").get_text().strip()

    def get_cost_string(self, soup):
        return soup.find(class_="wprm-recipe-recipe_cost").string

    def get_recipe_title(self, soup):
        return soup.find(class_="wprm-recipe-name").string
