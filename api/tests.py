import django.test
import requests
from datetime import datetime
from urllib import parse


SUCCESS_URL = "http://localhost:8000/api/v1/mpan/1200031039874/readings/"
SUCCESS_URL_FROM_DATE = (
    "http://localhost:8000/api/v1/mpan/1200023305967/readings/?from=2016-04-22"
)
SUCCESS_URL_TO_DATE = (
    "http://localhost:8000/api/v1/mpan/1200023305967/readings/?to=2016-02-23"
)
NOT_FOUND_URL = "http://localhost:8000/api/mpan/1200031039874/readings/"
SUCCESS_JSON = requests.get(SUCCESS_URL).json()
SUCCESS_JSON_FROM_DATE = requests.get(SUCCESS_URL_FROM_DATE).json()
SUCCESS_JSON_TO_DATE = requests.get(SUCCESS_URL_TO_DATE).json()


class TestAPIResponseCodes(django.test.TestCase):
    """Testing that API response codes are what we expect"""

    def test_success(self):
        """Ensure that 200 is received for a successful request"""
        req = requests.get(SUCCESS_URL)
        self.assertEqual(req.status_code, 200)

    def test_not_found(self):
        """Ensure that 404 is received when url does not match any routes"""
        req = requests.get(NOT_FOUND_URL)
        self.assertEqual(req.status_code, 404)


class TestJSONResponses(django.test.TestCase):
    """Testing that JSON responses from API are logical"""

    def test_mpan_matches_url(self):
        """Ensures that MPAN_CORE in each reading matches url"""
        reading_mpan = [r["mpan_core"] for r in SUCCESS_JSON["readings"]]
        self.assertEqual(reading_mpan[0], SUCCESS_JSON["mpan_core"])

    def test_filter_excludes_data_before(self):
        """Ensures readings before a FROM date are not included"""
        from_date = datetime.strptime(
            self._get_url_params(SUCCESS_URL_FROM_DATE)["from"][0], "%Y-%m-%d"
        )
        reading_dates = [
            datetime.strptime(d["reading_taken_at"], "%Y-%m-%dT%H:%M:%SZ")
            for d in [r for r in SUCCESS_JSON_FROM_DATE["readings"]]
        ]
        for date in reading_dates:
            with self.subTest(date=date):
                self.assertGreaterEqual(date, from_date)

    def test_filter_excludes_data_after(self):
        """Ensures readings AFTER a TO date are not included"""
        to_date = datetime.strptime(
            self._get_url_params(SUCCESS_URL_TO_DATE)["to"][0], "%Y-%m-%d"
        )
        reading_dates = [
            datetime.strptime(d["reading_taken_at"], "%Y-%m-%dT%H:%M:%SZ")
            for d in [r for r in SUCCESS_JSON_TO_DATE["readings"]]
        ]
        for date in reading_dates:
            with self.subTest(date=date):
                self.assertLessEqual(date, to_date)

    def _get_url_params(self, url: str) -> dict:
        parsed_url = parse.urlparse(url)
        return parse.parse_qs(parsed_url.query)
