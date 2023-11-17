from tech_news.database import db
from collections import Counter


# Requisito 10
def top_5_categories():
    news_categories = [news["category"] for news in db.news.find()]
    count_categories = Counter(news_categories)

    top_categories = sorted(
        count_categories.items(),
        key=lambda x: (-x[1], x[0]))[:5]

    top_5_categories = [category for category, _ in top_categories]

    return top_5_categories
