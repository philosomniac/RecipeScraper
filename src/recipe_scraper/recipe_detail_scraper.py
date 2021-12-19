import logging


from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag

from recipe_scraper import scraper_common
from recipe_scraper.models import Costs, Ingredient, IngredientSet, Recipe


class RecipeDetailScraper():
    """takes in a budgetbytes.com url OR an html file containing a budgetbytes.com
    recipe, and parses the information into a Recipe model"""

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
        # TODO: log events

        recipe_title = self._get_recipe_title(soup)

        cost_data = self._get_cost_data(soup)

        try:
            prep_time = self._get_prep_time(soup)
        except ElementNotFound:
            # some recipes don't have cook time
            prep_time = 0

        try:
            cook_time = self._get_cook_time(soup)
        except ElementNotFound:
            # some recipes don't have prep time
            cook_time = 0

        if cook_time == 0 and prep_time == 0:
            raise ElementNotFound("Could not get cook time or prep time")

        try:
            servings = self._get_servings(soup)
        except ElementNotFound:
            # assume single serving if servings element can't be found
            servings = 1

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

        cost_string = str(self._get_cost_string(soup))
        recipe_cost = self._get_recipe_cost_from_cost_string(cost_string)
        try:
            serving_cost = self._get_serving_cost_from_cost_string(
                cost_string)
        except ElementNotFound:
            # means the recipe_cost is the same as the serving cost
            serving_cost = recipe_cost

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

    # TODO: add support for recipes that have ingredients divided into named sections

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

    @staticmethod
    def _format_price(price_string: str) -> str:
        return price_string.replace("(", "").replace(")", "").replace("$", "").replace("*", "")

    @staticmethod
    def _get_ingredient_price(element):
        result = ""
        if isinstance(element, Tag):
            price_element = element.find(class_="wprm-recipe-ingredient-notes")
            if price_element is not None:
                result = price_element.string if isinstance(
                    price_element, Tag) else price_element

        if result is not None:
            return result
        else:
            return ""

    @staticmethod
    def _get_recipe_cost_from_cost_string(cost_string: str) -> float:
        recipe_word_index = cost_string.index('recipe')
        recipe_cost_string = cost_string[:recipe_word_index]
        recipe_cost_string = recipe_cost_string.replace("$", "")
        recipe_cost_string = recipe_cost_string.strip()
        recipe_cost = float(recipe_cost_string)
        return recipe_cost

    @staticmethod
    def _get_serving_cost_from_cost_string(cost_string: str) -> float:
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

    @staticmethod
    def _get_ingredient_name(element):
        result = ""
        if isinstance(element, Tag):
            ingredient_element = element.find(
                class_="wprm-recipe-ingredient-name")
            if ingredient_element is not None:
                result = ingredient_element.string if isinstance(
                    ingredient_element, Tag) else ingredient_element
                result = result.strip() if isinstance(result, str) else result
        return result

    @staticmethod
    def _get_current_unit(element: PageElement) -> str:
        result = ""
        if isinstance(element, Tag):
            unit_element = element.find(class_="wprm-recipe-ingredient-unit")
            if unit_element is not None:
                result = unit_element.string if isinstance(
                    unit_element, Tag) else str(unit_element)
        if result is not None:
            return result
        raise ElementNotFound("Could not get ingredient unit element")

    @staticmethod
    def _get_current_amount(element):
        amount = ""
        if isinstance(element, Tag):
            ingredient_tag = element.find(
                class_="wprm-recipe-ingredient-amount")
            if ingredient_tag is not None:
                if isinstance(ingredient_tag, Tag):
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

    @staticmethod
    def _get_ingredient_container(soup):
        return soup.find(class_="wprm-recipe-ingredients-container")

    @staticmethod
    def _get_img_url(soup):
        return soup.find(class_="wprm-recipe-image").img['src']

    @staticmethod
    def _get_servings_unit(soup):
        return soup.find(class_="wprm-recipe-servings-unit").string

    @staticmethod
    def _get_servings(soup):
        try:
            servings = int(soup.find(class_="wprm-recipe-servings").string)
            return servings
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

    @staticmethod
    def _parse_cook_time_string_to_minutes(cook_time_string: str) -> int:

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

    @staticmethod
    def _get_total_time(soup):
        return soup.find(class_="wprm-recipe-total-time-container")

    @staticmethod
    def _get_cost_string(soup):
        result = soup.find(class_="cost")
        if result:
            return result.string

        raise ElementNotFound("Could not find cost string")

    @staticmethod
    def _get_recipe_title(soup):
        result = soup.find(class_="wprm-recipe-name")
        if result:
            return result.string

        # old format
        old_format_result = soup.find(class_="post-title").h1
        if old_format_result:
            return old_format_result

        raise ElementNotFound("Could not find recipe title")


class ElementNotFound(Exception):
    """Raised when an element can't be found in the html"""


class CouldNotScrapeRecipe(Exception):
    """Raised when recipe scraping fails and could not be recovered"""
