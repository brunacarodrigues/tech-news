from tech_news.analyzer.reading_plan import ReadingPlanService  # noqa: F401, E261, E501
import pytest
from unittest.mock import patch


def test_reading_plan_group_news():
    reading_plan_service = ReadingPlanService()

    with pytest.raises(
        ValueError,
        match="Valor 'available_time' deve ser maior que zero"
    ):
        reading_plan_service.group_news_for_available_time(0)

    news_mock = [
        {"title": "Notícia 1", "reading_time": 4},
        {"title": "Notícia 2", "reading_time": 5},
        {"title": "Notícia 3", "reading_time": 15},
        {"title": "Notícia 4", "reading_time": 20},
    ]

    with patch(
        "tech_news.analyzer.reading_plan.find_news",
        return_value=news_mock
    ):
        result = reading_plan_service.group_news_for_available_time(10)

    assert result['readable']
    if result['readable']:
        readable_group = result['readable'][0]

    assert len(readable_group['chosen_news']) == 2
    assert readable_group['chosen_news'][0] == ('Notícia 1', 4)
    assert readable_group['chosen_news'][1] == ('Notícia 2', 5)
    assert readable_group['unfilled_time'] == 1

    assert len(result['unreadable']) == 2
    assert result['unreadable'][0] == ('Notícia 3', 15)
    assert result['unreadable'][1] == ('Notícia 4', 20)
