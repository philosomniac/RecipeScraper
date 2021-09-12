import logging
import re

from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

import scraper_common
from models.costs import Costs
from models.ingredient import Ingredient
from models.ingredient_set import IngredientSet
from models.recipe import Recipe


class RecipeDetailScraper():
    def get_recipe_details_from_url(self, url: str) -> Recipe:
        try:
            url = url.strip()
            logging.info(f"getting recipe details from url: {url}")
            soup = scraper_common.get_parsed_html_from_url(url)

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
        recipe_title = self._get_recipe_title(soup)

        # TODO: Parse the cost into real data
        cost_data = self._get_cost_data(soup)

        # TODO: Parse time strings into actual times
        # total_time = get_total_time(soup)
        try:
            prep_time = self._get_prep_time(soup)
        except ElementNotFound:
            # means there is no prep time
            prep_time = 0
        try:
            cook_time = self._get_cook_time(soup)
        except ElementNotFound:
            # means there is no cook time
            cook_time = 0

        if cook_time == 0 and prep_time == 0:
            raise ElementNotFound("Could not get cook time or prep time")

        try:
            servings = self._get_servings(soup)
        except ElementNotFound:
            # assume single serving if servings element can't be found
            servings = 1
        # servings_unit = get_servings_unit(soup)

        img_url = self._get_img_url(soup)

        current_ingredient_set = self._get_ingredient_set(soup)

        # TODO: get instruction set data and put into recipe class

        current_recipe = Recipe(
            url=url,
            name=recipe_title,
            ingredient_set=current_ingredient_set,
            total_cost=cost_data.recipe_cost,
            serving_cost=cost_data.serving_cost,
            servings=servings,
            prep_time=prep_time,
            cook_time=cook_time,
            img_url=img_url
        )
        return current_recipe

    def _get_cost_data(self, soup: BeautifulSoup) -> Costs:
        recipe_cost = None
        serving_cost = None
        try:
            cost_string = str(self._get_cost_string(soup))
            recipe_cost = self._get_recipe_cost_from_cost_string(cost_string)
            try:
                serving_cost = self._get_serving_cost_from_cost_string(
                    cost_string)
            except ElementNotFound:
                # means the recipe_cost is the same as the serving cost
                serving_cost = recipe_cost

        except ElementNotFound:
            raise

        costs = Costs(serving_cost, recipe_cost)
        return costs

    def _get_ingredient_set_from_elements(self, ingredient_elements):
        ingredient_list = []

        for ingredient_element in ingredient_elements:
            current_ingredient = self._get_ingredient_from_element(
                ingredient_element)
            ingredient_list.append(current_ingredient)

        current_ingredient_set = IngredientSet(ingredients=ingredient_list)
        return current_ingredient_set

    def _get_ingredient_set(self, soup):
        ingredient_elements = self._get_ingredient_elements(soup)
        return self._get_ingredient_set_from_elements(ingredient_elements)

    # TODO: unit test this

    # TODO: add support for ingredient sections

    def _get_ingredient_from_element(self, element: PageElement) -> Ingredient:
        current_amount = self._get_current_amount(element)
        current_unit = self._get_current_unit(element)
        current_name = self._get_ingredient_name(element)
        current_price = self._get_ingredient_price(element)
        current_price = float(self._format_price(current_price))

        current_ingredient = Ingredient(
            name=current_name,
            amount=current_amount,
            unit=current_unit,
            price=current_price
        )

        return current_ingredient

    def _get_recipe_urls(self, starting_line_index: int) -> list:
        with open("BudgetBytesRecipes.txt") as recipefile:
            recipe_urls = [line.strip() for line in recipefile]
            return recipe_urls[starting_line_index-1:]

    def _format_price(self, s: str) -> str:
        return s.replace("(", "").replace(")", "").replace("$", "").replace("*", "")

    def _get_ingredient_price(self, element):
        result = ""
        if isinstance(element, Tag):
            price_element = element.find(class_="wprm-recipe-ingredient-notes")
            if price_element is not None:
                result = price_element.string
        if result is not None:
            return result
        else:
            return ""

    def _get_recipe_cost_from_cost_string(self, cost_string: str) -> float:
        recipe_word_index = cost_string.index('recipe')
        recipe_cost_string = cost_string[:recipe_word_index]
        recipe_cost_string = recipe_cost_string.replace("$", "")
        recipe_cost_string = recipe_cost_string.strip()
        recipe_cost = float(recipe_cost_string)
        return recipe_cost

    def _get_serving_cost_from_cost_string(self, cost_string: str) -> float:
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

    def _get_ingredient_name(self, element):
        result = ""
        if isinstance(element, Tag):
            ingredient_element = element.find(
                class_="wprm-recipe-ingredient-name")
            if ingredient_element is not None:
                if ingredient_element.string is not None:
                    result = ingredient_element.string.strip()
        return result

    def _get_current_unit(self, element) -> str:
        result = ""
        if isinstance(element, Tag):
            unit_element = element.find(class_="wprm-recipe-ingredient-unit")
            if unit_element is not None:
                if unit_element.string is not None:
                    result = unit_element.string
        return result

    def _get_current_amount(self, element):
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

    def _get_ingredient_elements(self, soup):
        result = None
        ingredient_container = self._get_ingredient_container(soup)
        if isinstance(ingredient_container, Tag):
            result = ingredient_container.find_all(
                class_="wprm-recipe-ingredient")
        return result

    def _get_ingredient_container(self, soup):
        return soup.find(class_="wprm-recipe-ingredients-container")

    def _get_img_url(self, soup):
        return soup.find(class_="wprm-recipe-image").img['data-src']

    def _get_servings_unit(self, soup):
        return soup.find(class_="wprm-recipe-servings-unit").string

    def _get_servings(self, soup):
        try:
            return int(soup.find(class_="wprm-recipe-servings").string)
        except:
            ElementNotFound("Could not get servings")

    def _get_cook_time(self, soup):
        try:
            cook_time_string = soup.find(
                class_="wprm-recipe-cook-time-container").get_text().strip()
            return self._parse_cook_time_string_to_minutes(
                cook_time_string)

        except:
            raise ElementNotFound("Could not get Cook time")

    def _parse_cook_time_string_to_minutes(self, cook_time_string: str) -> int:

        hours_component_index = cook_time_string.find("hr")
        result_time = 0

        if hours_component_index != -1:
            hours_component = cook_time_string[:hours_component_index]

            hours_component = ''.join(
                c for c in hours_component if c.isdigit())
            if hours_component:
                result_time += int(hours_component) * 60
            minutes_component = cook_time_string[hours_component_index:]

            minutes_component = ''.join(
                c for c in minutes_component if c.isdigit())
            if minutes_component:
                result_time += int(minutes_component)

        else:
            cook_time_string = ''.join(
                c for c in cook_time_string if c.isdigit())
            result_time += int(cook_time_string)

        return result_time

    def _get_prep_time(self, soup):
        try:
            prep_time_string = soup.find(
                class_="wprm-recipe-prep-time-container").get_text()
            return self._parse_cook_time_string_to_minutes(prep_time_string)

        except:
            raise ElementNotFound("Could not get Prep time")

    def _get_total_time(self, soup):
        return soup.find(class_="wprm-recipe-total-time-container")

    def _get_cost_string(self, soup):
        result = soup.find(class_="wprm-recipe-recipe_cost")
        if result:
            return result.string
        else:
            raise ElementNotFound("Could not find cost string")

    def _get_recipe_title(self, soup):
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
