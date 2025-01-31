import unittest
from unittest.mock import MagicMock

from config.env import config
from service.scraper_service import ScrapperService, Location
from service.source_service import SourceService, Unauthorized


class TestScrapperService(unittest.TestCase):
    def setUp(self):
        self.mock_config = config
        self.scrapper_service = ScrapperService(self.mock_config)

        self.scrapper_service._logger = MagicMock()
        self.mock_source_service = MagicMock(spec=SourceService)

        self.scrapper_service._source_service = self.mock_source_service

    def test_get_today_access(self):
        self.mock_source_service.get_today_access.return_value = [{"test": "data"}]
        result = self.scrapper_service.get_today_access(Location.ESPACIO_URBANO.value)

        expected_result = [{"test": "data"}]

        self.mock_source_service.get_today_access.assert_called_once_with(
            Location.ESPACIO_URBANO.value
        )
        self.assertEqual(result, expected_result)

    def test_get_today_access_unauthorized(self):
        expected_result = [{"test": "data"}]
        self.mock_source_service.get_today_access.side_effect = [
            Unauthorized(),
            expected_result,
        ]

        result = self.scrapper_service.get_today_access(Location.ESPACIO_URBANO.value)

        self.mock_source_service.login.assert_called_once()
        self.assertEqual(result, expected_result)

    def test_get_today_access_exception(self):
        pass
