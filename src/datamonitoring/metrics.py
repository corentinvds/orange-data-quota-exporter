# coding=utf-8
import logging
import time
from typing import List

from prometheus_client import CollectorRegistry, start_http_server
from prometheus_client.metrics_core import GaugeMetricFamily

from datamonitoring.model import DataUnit
from datamonitoring.processor import get_web_usages

LOGGER = logging.getLogger(__name__)


class DownloadQuotaUsageCollector(object):
    def __init__(self, user: str, password: str, numbers: List[str]):
        self._user = user
        self._password = password
        self._numbers = numbers

    def collect(self):
        LOGGER.debug(f"Getting Orange info for numbers {self._numbers}")
        usage_gauge = GaugeMetricFamily(
            name='download_quota_usage',
            documentation='Internet quota usage',
            unit='bytes',
            labels=["number", "quota_name"],
        )
        limit_gauge = GaugeMetricFamily(
            name='download_quota_limit',
            documentation='Internet quota limit',
            unit='bytes',
            labels=["number", "quota_name"],
        )
        usages = get_web_usages(self._user, self._password, self._numbers)
        for usage in usages:
            usage_gauge.add_metric([usage.phone_number, usage.quota_name], usage.used_gb * DataUnit.GB.multiplier)
            limit_gauge.add_metric([usage.phone_number, usage.quota_name], usage.limit_gb * DataUnit.GB.multiplier)
        yield limit_gauge
        yield usage_gauge


def start_metric_server(port, user, password, numbers):
    registry = CollectorRegistry(auto_describe=False)
    registry.register(DownloadQuotaUsageCollector(user, password, numbers))
    start_http_server(port, registry=registry)
    LOGGER.info(f"Metrics server started on port {port}")
    while True:
        time.sleep(1)
