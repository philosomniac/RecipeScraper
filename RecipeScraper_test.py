import RecipeScraper


def test_get_recipe_urls_from_archive_page():
    test_page = "https://www.budgetbytes.com/archive/2010/07/"
    known_recipe_url = "https://www.budgetbytes.com/chipotle-peach-salsa/"

    urls = RecipeScraper.get_recipe_urls_from_archive_page(test_page)

    assert known_recipe_url in urls
