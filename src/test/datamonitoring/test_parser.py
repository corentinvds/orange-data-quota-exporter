# coding=utf-8
import os
from datetime import date, datetime
from os.path import dirname
from unittest import TestCase

import pytz
from lxml import html

from datamonitoring.model import Usage
from datamonitoring.parser import DashboardParser

BRUSSELS = pytz.timezone('Europe/Brussels')


class ParserTest(TestCase):
    def test_parse_file(self):
        with open(os.path.join(dirname(__file__), "testfile.html"), encoding="utf8") as f:
            html_content = html.fromstring(f.read())
            phone_number = DashboardParser._parse_phone_number(html_content)
            self.assertEqual(phone_number, "0493971508")

            usages = [u.to_dict() for u in DashboardParser.parse_usages(html_content)]

            expected_usages = [
                u.to_dict() for u in [
                    Usage(period_start=date(2020, 8, 15),
                          period_end=date(2020, 9, 14),
                          phone_number="0493971508",
                          quota_name="Volume de surf",
                          created=BRUSSELS.localize(datetime.now()),
                          updated=BRUSSELS.localize(datetime(2020, 8, 18, 19, 51)),
                          used_gb=0.0,
                          limit_gb=15.0,
                          id=None),

                    Usage(period_start=date(2020, 8, 15),
                          period_end=date(2020, 9, 14),
                          phone_number="0493971508",
                          quota_name="Data Boost heures pleines",
                          created=BRUSSELS.localize(datetime.now()),
                          updated=BRUSSELS.localize(datetime(2020, 8, 18, 19, 51)),
                          used_gb=8.0,
                          limit_gb=35.0,
                          id=None),

                    Usage(period_start=date(2020, 8, 15),
                          period_end=date(2020, 9, 14),
                          phone_number="0493971508",
                          quota_name="Data Boost heures creuses",
                          created=BRUSSELS.localize(datetime.now()),
                          updated=BRUSSELS.localize(datetime(2020, 8, 18, 19, 51)),
                          used_gb=19.1,
                          limit_gb=100.0,
                          id=None),
                ]
            ]

            # check created separately
            for i in range(max(len(expected_usages), len(usages))):
                expected_created = expected_usages[i].pop("created")
                actual_created = usages[i].pop("created")
                self.assertLess((expected_created - actual_created).total_seconds(), 10)

            self.assertEqual(expected_usages, usages)
