# coding=utf-8
import logging
from typing import List

from .crawler import WebCrawler
from .model import Usage
from .parser import DashboardParser

LOGGER = logging.getLogger(__name__)


def print_usages(user, password, numbers):
    LOGGER.debug("Getting Orange info ...")
    web_usages = get_web_usages(user, password, numbers)
    period_end, period_start = get_period(web_usages)
    LOGGER.info(f"Usages for period {period_start} -> {period_end}:\n - "
                + "\n - ".join([f"{u.to_dict()}" for u in web_usages]))


def get_web_usages(user: str, password: str, phone_numbers: List[str] = None) -> [Usage]:
    usages = []
    with WebCrawler(user, password).managed_resource() as crawler:
        crawler.login()
        for phone_number in phone_numbers or [None]:
            dashboard_html = crawler.get_dashboard(phone_number)
            usages += DashboardParser.parse_usages(dashboard_html)

    return usages


def get_period(web_usages):
    periods = {(u.period_start, u.period_end) for u in web_usages}
    if len(periods) != 1:
        raise Exception("Multiple period found: {}".format(periods))
    period_start, period_end = periods.pop()
    return period_end, period_start
