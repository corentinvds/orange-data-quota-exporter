from contextlib import contextmanager

import requests
from lxml import html

EXPECTED_WELCOME_MESSAGE = "Bonjour "


class WebCrawlerError(Exception):
    pass


class WebCrawler:

    def __init__(self, user: str, password: str):
        self._session = None
        self._user = user
        self._password = password

    @contextmanager
    def managed_resource(self):
        self.connect()
        try:
            yield self
        finally:
            self.close()

    def connect(self):
        self._session = requests.session()

    def _check_session(self):
        if not self._session:
            raise WebCrawlerError("Crawler not properly initialized (no session timestamp)")

    def login(self):
        self._check_session()

        payload = {
            'PASSWORD': self._password,
            'USER': self._user,
            'smauthreason': '/',
            'smretries': '0',
            'target': 'https://sso.orange.be/fr/home'
        }

        login_response = self._session.post(url="https://sso.orange.be/auth/sm/login.fcc", data=payload, verify=False)

        if EXPECTED_WELCOME_MESSAGE.upper() not in login_response.text.upper():
            raise WebCrawlerError("Cannot login! Response is \n " + login_response.text)

    def close(self):
        if self._session:
            self._session.close()
            self._session = None

    def get_dashboard(self, phone_number=None):
        self._check_session()
        url = "https://e-services.orange.be/fr/ajax/overview/postpaid_usage_dashboard/{}".format(phone_number or "")
        response = self._session.get(url)
        return html.fromstring(response.text)
