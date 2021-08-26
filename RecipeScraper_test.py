from Models.Recipe import Recipe
from Models.IngredientSet import IngredientSet
from Models.Ingredient import Ingredient
from RecipeDetailScraper import RecipeDetailScraper
from datetime import datetime
from RecipeURLRetriever import RecipeURLRetriever
import os
import filecmp
import ScraperCommon
import pytest
import json


@pytest.fixture
def retriever() -> RecipeURLRetriever:
    return RecipeURLRetriever()


@pytest.fixture
def detail_scraper() -> RecipeDetailScraper:
    return RecipeDetailScraper()


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


def test_scrape_full_recipe_url_list(retriever):
    test_file_path = "BudgetBytesRecipes_test.txt"
    month_limit = 8
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
    ingredient_elements = detail_scraper.get_ingredient_elements(soup)

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

    actual_ingredients = detail_scraper.get_ingredient_set(soup)

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


def test_parse_cost_string(detail_scraper: RecipeDetailScraper):
    test_cost_string = '$3.13 recipe / $0.78 serving'
    target_recipe_cost = 3.13
    target_serving_cost = 0.78
    actual_recipe_cost = detail_scraper.get_recipe_cost_from_cost_string(
        test_cost_string)

    assert target_recipe_cost == actual_recipe_cost

    actual_serving_cost = detail_scraper.get_serving_cost_from_cost_string(
        test_cost_string)
    assert target_serving_cost == actual_serving_cost


def test_recipe_to_json(sample_recipe: Recipe):
    json_ingredient = json.dumps(sample_recipe, default=lambda x: vars(x))
    pass
