"""Data collectors."""
from .company_collector import CompanyCollector
from .news_collector import NewsCollector
from .person_collector import PersonCollector

__all__ = ["CompanyCollector", "PersonCollector", "NewsCollector"]
