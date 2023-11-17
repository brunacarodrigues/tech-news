from tech_news.database import search_news
from datetime import datetime


# Requisito 7
def search_by_title(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    return [(new["title"], new["url"]) for new in search_news(query)]


# Requisito 8
def search_by_date(date):
    try:
        iso_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        raise ValueError("Data inválida")

    query = {"timestamp": iso_date}
    result_search_news = search_news(query)

    news = [(new["title"], new["url"]) for new in result_search_news]
    return news


# Requisito 9
def search_by_category(category):
    query = {"category": {"$regex": category, "$options": "i"}}
    return [(new["title"], new["url"]) for new in search_news(query)]
