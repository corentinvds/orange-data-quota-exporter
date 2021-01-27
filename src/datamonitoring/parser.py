# coding=utf8

import logging
import re
from datetime import datetime, date
from decimal import Decimal

from .dateutils import localized_now, localize
from .model import DataAmount, DataUnit, Usage

LOGGER = logging.getLogger(__name__)


class DashboardParserError(Exception):
    pass


class DashboardParser:

    @classmethod
    def parse_usages(cls, html_dashboard) -> [Usage]:
        phone_number = cls._parse_phone_number(html_dashboard)
        start, end = cls._parse_invoice_period(html_dashboard)
        usages = [
            Usage(start, end,
                  phone_number, title,
                  localized_now(), last_updated,
                  used_gb, limit_gb)
            for title, last_updated, limit_gb, used_gb in cls._parse_data_quotas(html_dashboard)
        ]
        return usages

    @staticmethod
    def _parse_phone_number(html_dashboard) -> str:
        return html_dashboard.xpath(
            "//div[@class='tariff-plan-info-inner']/div[@class='title']/span[@data-cs-mask]/text()")[0] \
            .strip().replace(" ", "")

    @classmethod
    def _parse_invoice_period(cls, html_dashboard) -> (date, date):
        period_str = html_dashboard.xpath("//div[@class='tariff-plan-info-inner']/div[@class='invoice-dates']")[
            0].text.strip()

        match = re.search(r"Ma consommation du (\d+/\d+/\d{4}) au (\d+/\d+/\d{4})", period_str)
        if not match:
            raise DashboardParserError("Invalid invoice period: " + period_str)
        else:
            return cls._parse_date(match.group(1)), cls._parse_date(match.group(2))

    @classmethod
    def _parse_data_quotas(cls, html_dashboard):
        balances = html_dashboard.xpath("//div[@class='meow-postpaid-balance']")

        for balance in balances:
            title = balance.xpath(".//div[@class='header-row clearfix']/strong/text()")[0].strip()
            last_updated = datetime.strptime(
                balance.xpath(".//span[@class='balance-updated']/text()")[0]
                    .replace("Mise à jour", "")
                    .strip(),
                "%d/%m/%Y %H:%M")
            last_updated = localize(last_updated)

            remaining_list = balance.xpath(".//div[@class='balance-remaining']/text()")
            consumed_list = balance.xpath(".//div[@class='unlimited-balance-consumed']/text()")

            if remaining_list:
                [remaining_amount, remaining_unit] = remaining_list[0].strip().split()[1:3]
                remaining = cls._parse_data_amount(remaining_amount, remaining_unit)

                limit_list = balance.xpath(".//div[@class='progress-bar-label-right']/text()")
                if limit_list:
                    [limit_amount, limit_unit] = limit_list[0].split("=")[0].split()
                    limit = cls._parse_data_amount(limit_amount, limit_unit)
                    used = limit - remaining
                else:
                    raise DashboardParserError("Missing limit for " + title)
            elif consumed_list:
                (used_amount, used_unit) = consumed_list[0].strip().split()[1:3]
                used = cls._parse_data_amount(used_amount, used_unit)
                limit = DataAmount(Decimal(100), DataUnit.GB)
            else:
                LOGGER.debug("ignored item: %s", title)
                continue
            yield title, last_updated, float(limit.get_value(DataUnit.GB)), float(used.get_value(DataUnit.GB))

    @staticmethod
    def _parse_date(str_date):
        return datetime.strptime(str_date, "%d/%m/%Y").date()

    @staticmethod
    def _parse_data_amount(amount: str, unit: str) -> DataAmount:
        return DataAmount(Decimal(amount.strip().replace(",", ".")), DataUnit[unit.strip().upper()])
