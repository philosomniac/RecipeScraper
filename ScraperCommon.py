from Models.IngredientSet import IngredientSet
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from Models.Recipe import Recipe
import json


TestSoupFilePath = "TestSoupFiles\\"


def get_parsed_html_from_url(url: str) -> BeautifulSoup:
    """Function: General scraping"""
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urlopen(req)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup


def save_html_from_url_to_file(url: str, file_name: str):
    soup = get_parsed_html_from_url(url)
    save_html_to_file(soup, file_name)


def get_html_from_test_file(file_name: str) -> BeautifulSoup:
    file_path = TestSoupFilePath + file_name
    with open(file_path, encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    return soup


def save_html_to_file(soup: BeautifulSoup, file_name: str):
    file_path = TestSoupFilePath + file_name
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, "w", encoding='utf-8') as output_file:
        output_file.write(str(soup))


def recipe_to_json(recipe: Recipe):
    return json.dumps(recipe, default=lambda x: vars(x))


def recipe_decode(json_to_decode):
    if 'ingredient_set' in json_to_decode:
        myIngredientSet = IngredientSet(
            json_to_decode['ingredient_set']['ingredients'])
        myRecipe = Recipe(**json_to_decode, ingredient_set=myIngredientSet)
        return myRecipe

    return json_to_decode


def json_to_recipe(recipe_json: str):
    j = json.loads(recipe_json, object_hook=recipe_decode)
    u = Recipe(**j)
    return u
