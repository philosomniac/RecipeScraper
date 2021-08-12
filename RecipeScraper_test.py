from datetime import datetime
from RecipeURLRetriever import RecipeURLRetriever
import os
import filecmp


def test_get_recipe_urls_from_archive_page():
    test_page = "https://www.budgetbytes.com/archive/2010/07/"
    known_recipe_urls = [
        "https://www.budgetbytes.com/chipotle-peach-salsa/",
        "https://www.budgetbytes.com/peach-almond-crisp/",
        "https://www.budgetbytes.com/breakfast-pizza/"
    ]

    retriever = RecipeURLRetriever()

    urls = retriever._get_recipe_urls_from_archive_page(test_page)

    assert all(elem in urls for elem in known_recipe_urls)


def test_get_archive_url_from_date():
    test_date = datetime(2015, 7, 10)
    url = "https://www.budgetbytes.com/archive/2015/07/"
    retriever = RecipeURLRetriever()
    result_url = retriever._get_archive_page_url_from_date(test_date)

    assert url == result_url


def test_scrape_full_recipe_URL_list():
    test_file_path = "BudgetBytesRecipes_test.txt"
    month_limit = 8
    retriever = RecipeURLRetriever()
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
    result_file = retriever.scrape_recipe_URL_list_to_file(
        test_file_path, month_limit)

    compare_file_path = "BudgetBytesRecipes_test_compare.txt"

    assert filecmp.cmp(test_file_path, compare_file_path, shallow=False)
