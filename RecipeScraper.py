from os import link
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


url = "https://www.budgetbytes.com/archive/2010/07"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(req)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# print(soup.get_text())

# image1, image2 = soup.find_all("img")

# print(image1["src"])

articlelist = soup.find_all("article")
linklist = []
for a in articlelist:
    # print(a)
    linklist.append(a.find("a"))

for l in linklist:
    print(l.get("href"))
