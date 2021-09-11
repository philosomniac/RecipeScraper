from RecipeDetailScraper import RecipeDetailScraper
import logging
from PersistenceHandler import PersistenceHandler


def setup_logging():
    logging.basicConfig(filename="recipescraper.log",
                        encoding="utf-8", level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')


def close_logging():
    logging.info('Finished')


def main():
    initialize()

    scrape_recipes(limit=10)

    close_logging()


def initialize():
    setup_logging()


def scrape_recipes(limit=999999, recipe_url_file_path="BudgetBytesRecipes.txt"):
    recipe_url_list = []
    with open(recipe_url_file_path, mode="r") as recipe_url_file:
        line_count = 0
        for line in recipe_url_file:
            if line_count >= limit:
                break
            recipe_url_list.append(line)
            line_count += 1

    detail_scraper = RecipeDetailScraper()
    persistence_handler = PersistenceHandler()
    for url in recipe_url_list:
        try:
            current_recipe = detail_scraper.get_recipe_details_from_url(url)

        except:
            logging.info(
                f"Could not retrieve recipe, continuing... url: {url}")
            continue

        try:
            if current_recipe:
                persistence_handler.save_recipe_to_persistence(current_recipe)
        except:
            logging.exception("Persistence error in saving recipe")


main()
