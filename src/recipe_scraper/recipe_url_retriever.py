import datetime
from urllib.error import HTTPError

from bs4 import BeautifulSoup
from bs4.element import PageElement, ResultSet, Tag
from dateutil.relativedelta import relativedelta

from recipe_scraper import scraper_common


class RecipeURLRetriever():
    """Scrapes a list of recipe URLs from budgetbytes.com and saves them to a file.
This is used as input to the detail_scraper module that scrapes each recipe URL 
and parses its details"""

    def scrape_recipe_URL_list_to_file(self, recipe_file_path: str = "BudgetBytesRecipes.txt", month_limit: int = 1000):

        recipe_url_list = []

        archive_start_date = datetime.date(2009, 11, 1)
        archive_end_date = datetime.date(
            datetime.date.today().year, datetime.date.today().month, 1)

        with open(recipe_file_path, 'w') as recipefile:
            for month_counter in range(0, month_limit):
                currentdate = datetime.date(
                    archive_start_date.year, archive_start_date.month, archive_start_date.day)
                currentdate = currentdate + \
                    relativedelta(months=+month_counter)
                if currentdate == archive_end_date:
                    break
                currentpage = self._get_archive_page_url_from_date(currentdate)
                recipe_url_list.extend(
                    self._get_recipe_urls_from_archive_page(currentpage))
                print("completed date: " + str(currentdate))

            recipefile.writelines(url + '\n' for url in recipe_url_list)
            return recipefile

    def _get_archive_page_url_from_date(self, targetdate: datetime.date) -> str:
        paddedmonth = str(targetdate.month).zfill(2)
        return "https://www.budgetbytes.com/archive/{0}/{1}/".format(targetdate.year, paddedmonth)

    def _get_recipe_urls_from_archive_page(self, archiveurl: str) -> list:
        url_list = []
        try:
            soup = scraper_common.get_parsed_html_from_url(archiveurl)
            article_elements = self._get_article_elements_from_page(soup)
            url_list.extend(
                self._get_article_urls_from_article_elements(article_elements))

            return url_list
        except HTTPError:
            return url_list

    def _get_article_elements_from_page(self, soup: BeautifulSoup) -> ResultSet:
        """Function: Retrieve Recipe List"""

        return soup.find_all("article")

    def _get_article_urls_from_article_elements(self, article_elements: ResultSet) -> list:
        url_list = []
        article_element: PageElement
        for article_element in article_elements:
            if isinstance(article_element, Tag):
                a_tag = article_element.find("a")
                if isinstance(a_tag, Tag):
                    url = a_tag.get("href")
                    url_list.append(url)

        return url_list
