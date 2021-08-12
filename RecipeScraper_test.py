from datetime import datetime
import RecipeScraper
from RecipeURLRetriever import RecipeURLRetriever


def test_get_recipe_urls_from_archive_page():
    test_page = "https://www.budgetbytes.com/archive/2010/07/"
    known_recipe_urls = [
        "https://www.budgetbytes.com/chipotle-peach-salsa/",
        "https://www.budgetbytes.com/peach-almond-crisp/",
        "https://www.budgetbytes.com/breakfast-pizza/"
    ]

    retriever = RecipeURLRetriever()

    urls = retriever.get_recipe_urls_from_archive_page(test_page)

    assert all(elem in urls for elem in known_recipe_urls)


def test_get_archive_url_from_date():
    test_date = datetime(2015, 7, 10)
    url = "https://www.budgetbytes.com/archive/2015/07/"
    retriever = RecipeURLRetriever()
    result_url = retriever.get_archive_page_url_from_date(test_date)

    assert url == result_url
