import unittest

from service.transformer_service import TransformerService


class TestTransformerService(unittest.TestCase):
    def test_response_access_to_spl_access(self):
        input_dict = {
            "IDCONTACTO": "123",
            "RUT": "12345678-9",
            "SOCIO": "Juan Perez",
            "FECHA": "2025-01-23",
            "TURNOINI": "08:00:00",
            "TURNOFIN": "09:00:00",
        }

        result = TransformerService.transform_response_access_to_spl_access(input_dict)

        expected_response = {
            "externalId": "123",
            "run": "12345678-9",
            "fullName": "Juan Perez",
            "entryAt": "2025-01-23T08:00:00-0300",
            "exitAt": "2025-01-23T09:00:00-0300",
        }

        self.assertEqual(result, expected_response)

    def test_response_access_to_spl_access_no_exit(self):
        input_dict1 = {
            "IDCONTACTO": "123",
            "RUT": "12345678-9",
            "SOCIO": "Juan Perez",
            "FECHA": "2025-01-23",
            "TURNOINI": "08:00:00",
            "TURNOFIN": None,
        }

        input_dict2 = {
            "IDCONTACTO": "123",
            "RUT": "12345678-9",
            "SOCIO": "Juan Perez",
            "FECHA": "2025-01-23",
            "TURNOINI": "08:00:00",
            "TURNOFIN": "",
        }

        result1 = TransformerService.transform_response_access_to_spl_access(
            input_dict1
        )
        result2 = TransformerService.transform_response_access_to_spl_access(
            input_dict2
        )

        expected_response1 = {
            "externalId": "123",
            "run": "12345678-9",
            "fullName": "Juan Perez",
            "entryAt": "2025-01-23T08:00:00-0300",
            "exitAt": None,
        }
        expected_response2 = {
            "externalId": "123",
            "run": "12345678-9",
            "fullName": "Juan Perez",
            "entryAt": "2025-01-23T08:00:00-0300",
            "exitAt": None,
        }

        self.assertEqual(result1, expected_response1)
        self.assertEqual(result2, expected_response2)


if __name__ == "__main__":
    unittest.main()
