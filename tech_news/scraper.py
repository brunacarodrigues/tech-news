import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    headers = {"user-agent": "Fake user-agent"}
    time.sleep(1)

    try:
        response = requests.get(url, headers=headers, timeout=3)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.Timeout:
        return None


# Requisito 2
def scrape_updates(html_content):
    selector = Selector(text=html_content)
    news_links = selector.css("div.entry-thumbnail a::attr(href)").getall()
    return news_links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    next_page_link = selector.css("div.nav-links a.next::attr(href)").get()
    return next_page_link


# Requisito 4
def scrape_news(html_content):
    selector = Selector(text=html_content)

    url = selector.css("link[rel='canonical']::attr(href)").get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css("span.author > a::text").get()
    reading_time = int(
        selector.css("li.meta-reading-time::text").re_first(r"\d+")
    )
    summary = (
        selector.css("div.entry-content > p:first-of-type")
        .xpath("string()")
        .get()
        .strip()
    )
    category = selector.css("a.category-style > span.label::text").get()
    print(category)

    news_data = {
        "url": url,
        "title": title,
        "timestamp": timestamp,
        "writer": writer,
        "reading_time": reading_time,
        "summary": summary,
        "category": category,
    }

    return news_data


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com"
    news_list = []

    while len(news_list) < amount:
        html_content = fetch(url)
        if html_content is None:
            break

        news_list.extend(scrape_updates(html_content))
        url = scrape_next_page_link(html_content)

    news_to_scrape = news_list[:amount]
    scraped_news = [scrape_news(fetch(news)) for news in news_to_scrape]

    create_news(scraped_news)
    return scraped_news
