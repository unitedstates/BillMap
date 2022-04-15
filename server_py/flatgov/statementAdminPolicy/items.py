# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem

from bills.models import Statement


class StatementadminpolicyItem(DjangoItem):
    # define the fields for your item here like:
    django_model = Statement
