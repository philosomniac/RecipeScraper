import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from bs4.element import PageElement, ResultSet, Tag
from urllib.error import HTTPError

import ScraperCommon


class RecipeURLRetriever():

    def get_archive_page_url_from_date(self, targetdate: datetime.date) -> str:
        """Function: Retrieve Recipe List"""
        paddedmonth = str(targetdate.month).zfill(2)
        return "https://www.budgetbytes.com/archive/{0}/{1}/".format(targetdate.year, paddedmonth)

    def get_recipe_urls_from_archive_page(self, archiveurl: str) -> list:
        """Function: Retrieve Recipe List"""
        url_list = []
        try:
            soup = ScraperCommon.get_parsed_html_from_url(archiveurl)
            article_elements = self.get_article_elements_from_page(soup)
            url_list.extend(
                self.get_article_urls_from_article_elements(article_elements))

            return url_list
        except HTTPError:
            return url_list

    def get_article_elements_from_page(self, soup: BeautifulSoup) -> ResultSet:
        """Function: Retrieve Recipe List"""

        return soup.find_all("article")

    def get_article_urls_from_article_elements(self, article_elements: ResultSet) -> list:
        """Function: Retrieve Recipe List"""
        url_list = []
        article_element: PageElement
        for article_element in article_elements:
            if isinstance(article_element, Tag):
                a_tag = article_element.find("a")
                if isinstance(a_tag, Tag):
                    url = a_tag.get("href")
                    url_list.append(url)

        return url_list

    def scrape_full_recipe_URL_list(self, recipe_file_path):
        """Function: Retrieve Recipe List"""

        recipe_url_list = []

        archive_start_date = datetime.date(2009, 5, 1)
        archive_end_date = datetime.date(
            datetime.date.today().year, datetime.date.today().month, 1)

        with open(recipe_file_path, 'w') as recipefile:
            for i in range(0, 1000):
                currentdate = datetime.date(
                    archive_start_date.year, archive_start_date.month, archive_start_date.day)
                currentdate = currentdate + relativedelta(months=+i)
                if currentdate == archive_end_date:
                    break
                currentpage = self.get_archive_page_url_from_date(currentdate)
                recipe_url_list.extend(
                    self.get_recipe_urls_from_archive_page(currentpage))
                print("completed date: " + str(currentdate))

            recipefile.writelines(l + '\n' for l in recipe_url_list)
