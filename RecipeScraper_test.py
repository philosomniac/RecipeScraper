import filecmp
import os
from datetime import datetime

import pytest

import ScraperCommon
from models.Ingredient import Ingredient
from models.IngredientSet import IngredientSet
from models.Recipe import Recipe
from PersistenceHandler import PersistenceHandler
from RecipeDetailScraper import ElementNotFound, RecipeDetailScraper
from RecipeURLRetriever import RecipeURLRetriever


@pytest.fixture
def retriever() -> RecipeURLRetriever:
    return RecipeURLRetriever()


@pytest.fixture
def detail_scraper() -> RecipeDetailScraper:
    return RecipeDetailScraper()


@pytest.fixture()
def persistence() -> PersistenceHandler:
    return PersistenceHandler()


@pytest.fixture()
def recipe_json_list() -> list[str]:
    json_list = [
        '{"url": "https://www.budgetbytes.com/lemon-garlic-roasted-asparagus/", "name": "Lemon Garlic Roasted Asparagus", "ingredient_set": {"ingredients": [{"name": "asparagus (1 lb.)", "amount": "1", "unit": "bunch", "price": 1.88}, {"name": "garlic", "amount": "2", "unit": "cloves", "price": 0.16}, {"name": "olive oil", "amount": "1", "unit": "tbsp", "price": 0.16}, {"name": "salt", "amount": "1/8", "unit": "tsp", "price": 0.02}, {"name": "freshly cracked black pepper", "amount": "1/8", "unit": "tsp", "price": 0.89}, {"name": "fresh lemon", "amount": "1", "unit": "", "price": 0.89}]}, "total_cost": 3.13, "serving_cost": 0.78, "servings": 4, "prep_time": 10, "cook_time": 20, "instruction_set": null, "img_url": "https://www.budgetbytes.com/wp-content/uploads/2011/03/Lemon-Garlic-Roasted-Asparagus-pan-200x200.jpg"}',
        '{"url": "https://www.budgetbytes.com/parmesan-roasted-potatoes/", "name": "Parmesan Roasted Potatoes", "ingredient_set": {"ingredients": [{"name": "russet or red potatoes", "amount": "2", "unit": "lbs", "price": 1.2}, {"name": "chopped fresh parsley", "amount": "1/4", "unit": "cup", "price": 0.2}, {"name": "olive oil", "amount": "2", "unit": "Tbsp", "price": 0.32}, {"name": "grated Parmesan", "amount": "1/3", "unit": "cup", "price": 0.55}, {"name": "garlic powder", "amount": "1/2", "unit": "tsp", "price": 0.05}, {"name": "Salt and pepper to taste", "amount": "", "unit": "", "price": 0.05}]}, "total_cost": 2.37, "serving_cost": 0.59, "servings": 4, "prep_time": 15, "cook_time": 40, "instruction_set": null, "img_url": "https://www.budgetbytes.com/wp-content/uploads/2009/11/Parmesan-Roasted-Potatoes-dip-200x200.jpg"}',
        '{"url": "https://www.budgetbytes.com/pepperoni-stuffed-chicken/", "name": "Pepperoni Stuffed Chicken", "ingredient_set": {"ingredients": [{"name": "boneless, skinless chicken breasts", "amount": "1", "unit": "lb", "price": 1.98}, {"name": "mozzarella cheese", "amount": "2", "unit": "oz", "price": 0.4}, {"name": "approx. 16 slices pepperoni", "amount": "1 1/4", "unit": "oz", "price": 0.54}, {"name": "large egg", "amount": "1", "unit": "", "price": 0.15}, {"name": "all purpose flour", "amount": "1/2", "unit": "cup", "price": 0.14}, {"name": "breadcrumbs", "amount": "1/2", "unit": "cup", "price": 0.18}, {"name": "vegetable oil", "amount": "6", "unit": "Tbsp", "price": 0.22}, {"name": "to taste salt and pepper", "amount": "", "unit": "", "price": 0.05}]}, "total_cost": 3.66, "serving_cost": 0.91, "servings": 4, "prep_time": 15, "cook_time": 30, "instruction_set": null, "img_url": "https://www.budgetbytes.com/wp-content/uploads/2009/12/Pepperoni20Stuffed20Chicken-200x200.jpg"}',
        '{"url": "https://www.budgetbytes.com/mexican-lentil-stew/", "name": "Mexican Red Lentil Stew", "ingredient_set": {"ingredients": [{"name": "dry red lentils", "amount": "2", "unit": "cups", "price": 3.46}, {"name": "olive oil", "amount": "1", "unit": "Tbsp", "price": 0.16}, {"name": "medium onion", "amount": "1", "unit": "", "price": 0.37}, {"name": "stalks celery", "amount": "3-4", "unit": "", "price": 0.79}, {"name": "garlic", "amount": "4", "unit": "cloves", "price": 0.32}, {"name": "fire roasted diced tomatoes", "amount": "2 14.5 oz", "unit": "cans", "price": 2.38}, {"name": "chili powder", "amount": "1/2", "unit": "Tbsp", "price": 0.15}, {"name": "cumin", "amount": "1", "unit": "tsp", "price": 0.1}, {"name": "turmeric", "amount": "1/2", "unit": "tsp", "price": 0.05}, {"name": "vegetable broth", "amount": "4", "unit": "cups", "price": 0.52}, {"name": "dashes hot sauce", "amount": "10-15", "unit": "", "price": 0.15}, {"name": "medium lime", "amount": "1", "unit": "", "price": 0.39}, {"name": "bunch cilantro", "amount": "1/2", "unit": "", "price": 0.5}]}, "total_cost": 9.34, "serving_cost": 1.33, "servings": 7, "prep_time": 10, "cook_time": 40, "instruction_set": null, "img_url": "https://www.budgetbytes.com/wp-content/uploads/2009/12/Mexican-Red-Lentil-Stew-above-1-200x200.jpg"}',
        '{"url": "https://www.budgetbytes.com/egg-florentine-quesadillas/", "name": "Egg Florentine Quesadillas", "ingredient_set": {"ingredients": [{"name": "6\u2033, 8\u2033 or 10\u2033 diameter your preference flour tortilla", "amount": "1", "unit": "", "price": 0.08}, {"name": "large egg", "amount": "1", "unit": "", "price": 0.15}, {"name": "creamed spinach", "amount": "1/4", "unit": "cup", "price": 0.28}, {"name": "shredded cheddar cheese", "amount": "2", "unit": "Tbsp", "price": 0.12}]}, "total_cost": 0.63, "serving_cost": 0.63, "servings": 1, "prep_time": 0, "cook_time": 10, "instruction_set": null, "img_url": "https://www.budgetbytes.com/wp-content/uploads/2009/12/Eggs20Florentine20Quesadilla201-200x200.jpg"}'
    ]
    return json_list


@pytest.fixture
def sample_recipe() -> Recipe:
    target_ingredients = [
        Ingredient("asparagus (1 lb.)", "1", "bunch", float("1.88")),
        Ingredient("garlic", "2", "cloves", float("0.16")),
        Ingredient("olive oil", "1", "tbsp", float("0.16")),
        Ingredient("salt", "1/8", "tsp", float("0.02")),
        Ingredient("freshly cracked black pepper",
                   "1/8", "tsp", float("0.89")),
        Ingredient("fresh lemon", "1", "", float("0.89"))
    ]
    target_ingredient_set = IngredientSet(target_ingredients)
    url = "https://www.budgetbytes.com/lemon-garlic-roasted-asparagus/"
    name = "Lemon Garlic Roasted Asparagus"
    total_cost = 3.13
    serving_cost = 0.78
    servings = 4
    prep_time_mins = 10
    cook_time_mins = 20
    # total_time_mins = 30
    img_url = "https://www.budgetbytes.com/wp-content/uploads/2011/03/Lemon-Garlic-Roasted-Asparagus-pan-200x200.jpg"
    return Recipe(
        url,
        name,
        target_ingredient_set,
        total_cost,
        serving_cost,
        servings,
        prep_time_mins,
        cook_time_mins,
        None,
        img_url
    )


def test_get_recipe_urls_from_archive_page(retriever):
    test_page = "https://www.budgetbytes.com/archive/2010/07/"
    known_recipe_urls = [
        "https://www.budgetbytes.com/chipotle-peach-salsa/",
        "https://www.budgetbytes.com/peach-almond-crisp/",
        "https://www.budgetbytes.com/breakfast-pizza/"
    ]

    urls = retriever._get_recipe_urls_from_archive_page(test_page)

    assert all(elem in urls for elem in known_recipe_urls)


def test_get_archive_url_from_date(retriever):
    test_date = datetime(2015, 7, 10)
    url = "https://www.budgetbytes.com/archive/2015/07/"
    result_url = retriever._get_archive_page_url_from_date(test_date)

    assert url == result_url


def test_scrape_full_recipe_url_list(retriever: RecipeURLRetriever):
    test_file_path = "BudgetBytesRecipes_test.txt"
    month_limit = 2
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
    _ = retriever.scrape_recipe_URL_list_to_file(
        test_file_path, month_limit)

    compare_file_path = "BudgetBytesRecipes_test_compare.txt"

    assert filecmp.cmp(test_file_path, compare_file_path, shallow=False)


def test_save_soup_to_file():
    test_recipe_url = "https://www.budgetbytes.com/lemon-garlic-roasted-asparagus/"
    ScraperCommon.save_html_from_url_to_file(
        test_recipe_url, "Test_Lemon_Garlic_Asparagus.txt")


def test_get_soup_from_test_file():
    test_file_name = "Test_elements.txt"
    print(os.getcwd())
    _ = ScraperCommon.get_html_from_test_file(test_file_name)


def test_get_ingredient_elements(detail_scraper):
    test_recipe_url = "https://www.budgetbytes.com/lemon-garlic-roasted-asparagus/"
    soup = ScraperCommon.get_parsed_html_from_url(test_recipe_url)
    ingredient_elements = detail_scraper._get_ingredient_elements(soup)

    ScraperCommon.save_html_to_file(ingredient_elements, "Test_elements.txt")


def test_get_ingredient_list_from_html(detail_scraper: RecipeDetailScraper):
    test_html_file = "Test_Lemon_Garlic_Asparagus.txt"
    soup = ScraperCommon.get_html_from_test_file(test_html_file)

    target_ingredients = [
        Ingredient("asparagus (1 lb.)", "1", "bunch", float("1.88")),
        Ingredient("garlic", "2", "cloves", float("0.16")),
        Ingredient("olive oil", "1", "tbsp", float("0.16")),
        Ingredient("salt", "1/8", "tsp", float("0.02")),
        Ingredient("freshly cracked black pepper",
                   "1/8", "tsp", float("0.89")),
        Ingredient("fresh lemon", "1", "", float("0.89"))
    ]
    target_ingredient_set = IngredientSet(target_ingredients)

    actual_ingredients = detail_scraper._get_ingredient_set(soup)

    assert target_ingredient_set == actual_ingredients


def test_get_recipe_detail_functions(sample_recipe: Recipe, detail_scraper: RecipeDetailScraper):
    test_html_file = "Test_Lemon_Garlic_Asparagus.txt"
    test_recipe_url = "https://www.budgetbytes.com/lemon-garlic-roasted-asparagus/"
    soup = ScraperCommon.get_html_from_test_file(test_html_file)
    scraped_recipe = detail_scraper.get_recipe_details_from_html(
        soup, test_recipe_url)

    assert scraped_recipe.url == sample_recipe.url
    assert scraped_recipe.name == sample_recipe.name
    assert scraped_recipe.total_cost == sample_recipe.total_cost
    assert scraped_recipe.serving_cost == sample_recipe.serving_cost
    assert scraped_recipe.servings == sample_recipe.servings
    assert scraped_recipe.ingredient_set == sample_recipe.ingredient_set
    assert scraped_recipe.cook_time == sample_recipe.cook_time
    assert scraped_recipe.prep_time == sample_recipe.prep_time
    assert scraped_recipe.img_url == sample_recipe.img_url


def test_scraping_non_recipe_should_throw_error(detail_scraper: RecipeDetailScraper):
    non_recipe_file = 'Soup_File_Non_Recipe.txt'

    with pytest.raises(ElementNotFound):
        soup = ScraperCommon.get_html_from_test_file(non_recipe_file)
        detail_scraper.get_recipe_details_from_html(soup)


def test_scraping_cook_times_with_hours_component(detail_scraper: RecipeDetailScraper):
    test_url = "https://www.budgetbytes.com/homemade-marinara/"
    test_recipe = detail_scraper.get_recipe_details_from_url(test_url)

    expected_cook_time = 90
    expected_total_time = 100

    assert test_recipe.cook_time == expected_cook_time
    assert test_recipe.cook_time + test_recipe.prep_time == expected_total_time


def test_scraping_recipe_with_no_cook_time(detail_scraper: RecipeDetailScraper):
    url = "https://www.budgetbytes.com/thai-peanut-sauce/"
    recipe = detail_scraper.get_recipe_details_from_url(url)

    expected_cook_time = 0
    expected_prep_time = 15
    assert recipe.cook_time == expected_cook_time
    assert recipe.prep_time == expected_prep_time


def test_parse_cost_string(detail_scraper: RecipeDetailScraper):
    test_cost_string = '$3.13 recipe / $0.78 serving'
    target_recipe_cost = 3.13
    target_serving_cost = 0.78
    actual_recipe_cost = detail_scraper._get_recipe_cost_from_cost_string(
        test_cost_string)

    assert target_recipe_cost == actual_recipe_cost

    actual_serving_cost = detail_scraper._get_serving_cost_from_cost_string(
        test_cost_string)
    assert target_serving_cost == actual_serving_cost


def test_recipe_to_json(sample_recipe: Recipe):

    compare_recipe_json = """\
{"url": "https://www.budgetbytes.com/lemon-garlic-roasted-asparagus/", "name": "Lemon Garlic Roasted Asparagus", "ingredient_set": {"ingredients": [{"name": "asparagus (1 lb.)", "amount": "1", "unit": "bunch", "price": 1.88}, {"name": "garlic", "amount": "2", "unit": "cloves", "price": 0.16}, {"name": "olive oil", "amount": "1", "unit": "tbsp", "price": 0.16}, {"name": "salt", "amount": "1/8", "unit": "tsp", "price": 0.02}, {"name": "freshly cracked black pepper", "amount": "1/8", "unit": "tsp", "price": 0.89}, {"name": "fresh lemon", "amount": "1", "unit": "", "price": 0.89}]}, "total_cost": 3.13, "serving_cost": 0.78, "servings": 4, "prep_time": 10, "cook_time": 20, "instruction_set": null, "img_url": "https://www.budgetbytes.com/wp-content/uploads/2011/03/Lemon-Garlic-Roasted-Asparagus-pan-200x200.jpg"}\
"""

    recipe_json = sample_recipe.to_json()

    assert recipe_json == compare_recipe_json


def test_json_to_recipe(sample_recipe: Recipe):
    recipe_json = """\
{"url": "https://www.budgetbytes.com/lemon-garlic-roasted-asparagus/", "name": "Lemon Garlic Roasted Asparagus", "ingredient_set": {"ingredients": [{"name": "asparagus (1 lb.)", "amount": "1", "unit": "bunch", "price": 1.88}, {"name": "garlic", "amount": "2", "unit": "cloves", "price": 0.16}, {"name": "olive oil", "amount": "1", "unit": "tbsp", "price": 0.16}, {"name": "salt", "amount": "1/8", "unit": "tsp", "price": 0.02}, {"name": "freshly cracked black pepper", "amount": "1/8", "unit": "tsp", "price": 0.89}, {"name": "fresh lemon", "amount": "1", "unit": "", "price": 0.89}]}, "total_cost": 3.13, "serving_cost": 0.78, "servings": 4, "prep_time": 10, "cook_time": 20, "instruction_set": null, "img_url": "https://www.budgetbytes.com/wp-content/uploads/2011/03/Lemon-Garlic-Roasted-Asparagus-pan-200x200.jpg"}\
"""

    test_recipe = Recipe.from_json(recipe_json)

    assert test_recipe == sample_recipe


def test_save_recipe_to_persistence(persistence: PersistenceHandler, sample_recipe: Recipe):
    persistence.save_recipe_to_persistence(sample_recipe)
    assert persistence.count_recipes_with_url(sample_recipe.url) == 1


def test_save_multiple_recipes_to_persistence(persistence: PersistenceHandler, recipe_json_list: list[str]):
    recipe_list = []

    for recipe_json_str in recipe_json_list:
        recipe = Recipe.from_json(recipe_json_str)
        recipe_list.append(recipe)

    persistence.save_recipes_to_persistence(recipe_list)

    for recipe in recipe_list:
        assert persistence.count_recipes_with_url(recipe.url) == 1


def test_get_recipe_from_persistence(persistence: PersistenceHandler):
    url = 'https://www.budgetbytes.com/mexican-lentil-stew/'
    recipe = persistence.get_recipe_by_url(url)

    assert recipe.name == "Mexican Red Lentil Stew"
    assert recipe.url == url


def test_save_duplicate_recipe_to_persistence(persistence: PersistenceHandler):
    url = 'https://www.budgetbytes.com/mexican-lentil-stew/'
    recipe = persistence.get_recipe_by_url(url)

    persistence.save_recipe_to_persistence(recipe)
    persistence.save_recipe_to_persistence(recipe)
    persistence.save_recipes_to_persistence([recipe])

    assert persistence.count_recipes_with_url("not a real url") == 0
    assert persistence.count_recipes_with_url(url) == 1


def test_save_existing_recipe_should_modify_recipe(persistence: PersistenceHandler):
    url = 'https://www.budgetbytes.com/mexican-lentil-stew/'
    recipe = persistence.get_recipe_by_url(url)

    original_prep_time = recipe.prep_time
    modified_prep_time = original_prep_time + 1

    recipe.prep_time = modified_prep_time
    persistence.save_recipe_to_persistence(recipe)
    modified_recipe = persistence.get_recipe_by_url(url)
    assert modified_recipe.prep_time == modified_prep_time
