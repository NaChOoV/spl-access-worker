import logging
import requests


class AccessService:
    def __init__(self, config: dict):
        self._base_url: str = config["SPL_ACCESS_BASE_URL"]
        self._token: str = config["SPL_ACCESS_TOKEN"]
        self._logger = logging.getLogger(self.__class__.__name__)

    def send_access(self, access: list[dict]):
        response = requests.post(
            f"{self._base_url}/api/access",
            headers={"X-Auth-Token": self._token},
            json={"data": access},
        )

        if response.status_code != 200:
            response.raise_for_status()
