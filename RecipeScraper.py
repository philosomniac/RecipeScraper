import logging


def setup_logging():
    """Function: Application"""
    logging.basicConfig(filename="recipescraper.log",
                        encoding="utf-8", level=logging.INFO, format='%(asctime)s %(message)s')
    logging.info('Started')


def close_logging():
    """Function: Application"""
    logging.info('Finished')


def Main():
    setup_logging()

    # my_recipes = []
    # recipe_urls = []
    # startline = 3
    # recipe_urls = get_recipe_urls(startline)

    # for i in range(10):
    #     # current_recipe = get_recipe_details_from_url(recipe_urls[i])
    #     pass

    # recipe_file_path = "BudgetBytesRecipes.txt"

    close_logging()


# Main()
