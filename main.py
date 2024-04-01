import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://zaicevvv1991:mysecretpassword@mymongodb.mby1agw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
    server_api=ServerApi("1"),
)

db = client.scrap
base_url = "https://quotes.toscrape.com"


def scrap_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all("small", class_="author")
    links = [author.find_next_sibling("a").get("href") for author in authors]
    tags = soup.find_all("div", class_="tags")
    get_quotes(quotes, authors, tags)
    get_authors(links)
    try:
        next_page = soup.find_all("li", class_="next")[0].find("a").get("href")
        print(f"Next page scraping: {base_url + next_page}")
        scrap_page(base_url + next_page)
    except Exception as e:
        print(f"[Warning]: No more next pages, {e}")


quotes_data = []
authors_data = []


def get_quotes(quotes, authors, tags):
    for i in range(0, len(quotes)):
        quotes_data.append(
            {
                "tags": [el.text.strip() for el in tags[i].find_all("a", class_="tag")],
                "author": authors[i].text.strip(),
                "quote": quotes[i].text.strip(),
            }
        )


def get_authors(links):
    for link in links:
        response = requests.get(base_url + link)
        soup = BeautifulSoup(response.text, features="html.parser")
        details = soup.select("div.author-details")
        fullname = details[0].find("h3").text.strip()
        born_date = details[0].select("span.author-born-date")[0].text.strip()
        born_location = details[0].select("span.author-born-location")[0].text.strip()
        description = details[0].select("div.author-description")[0].text.strip()
        authors_data.append(
            {
                "fullname": fullname,
                "born_date": born_date,
                "born_location": born_location,
                "description": description,
            }
        )


if __name__ == "__main__":
    scrap_page(base_url)

    with open("quotes.json", "w", encoding="utf-8") as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=2)

    with open("authors.json", "w", encoding="utf-8") as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=2)

    with open("quotes.json", "r", encoding="utf-8") as f:
        db.quotes.insert_many(json.load(f))

    with open("authors.json", "r", encoding="utf-8") as f:
        db.authors.insert_many(json.load(f))
