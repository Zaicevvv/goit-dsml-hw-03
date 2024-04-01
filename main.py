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

url = "https://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, features="html.parser")
quotes = soup.find_all("span", class_="text")
authors = soup.find_all("small", class_="author")
links = [author.find_next_sibling("a").get("href") for author in authors]
tags = soup.find_all("div", class_="tags")

quotes_data = []
for i in range(0, len(quotes)):
    quotes_data.append(
        {
            "tags": [el.text.strip() for el in tags[i].find_all("a", class_="tag")],
            "author": authors[i].text.strip(),
            "quote": quotes[i].text.strip(),
        }
    )

authors_data = []
for link in links:
    response = requests.get(url + link)
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

# with open("quotes.json", "w", encoding="utf-8") as f:
#     json.dump(quotes_data, f, ensure_ascii=False, indent=2)

# with open("authors.json", "w", encoding="utf-8") as f:
#     json.dump(authors_data, f, ensure_ascii=False, indent=2)

# with open("quotes.json", "r", encoding="utf-8") as f:
#     db.quotes.insert_many(json.load(f))

# with open("authors.json", "r", encoding="utf-8") as f:
#     db.authors.insert_many(json.load(f))
