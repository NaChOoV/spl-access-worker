from requests.cookies import RequestsCookieJar
import requests
from datetime import datetime
import re
import json
import logging


class SourceService:
    def __init__(self, config: dict[str, str]):
        self._config: dict[str, str] = config

        self._logger = logging.getLogger(self.__class__.__name__)
        self._base_url: str = config["SOURCE_BASE_URL"]
        self._cookies: RequestsCookieJar = None

    def login(self):
        form_data = {
            "LOGIN": self._config["SOURCE_USERNAME"],
            "CLAVE": self._config["SOURCE_PASSWORD"],
        }
        headers = {"user-agent": ""}

        response = requests.post(
            f"{self._base_url}/login_servidor.php", data=form_data, headers=headers
        )

        if not response.json()["estado"]["sesion"]:
            response.raise_for_status()

        self._cookies = response.cookies
        self._logger.info("Logged in successfully")
        return response

    def get_today_access(self):
        today = datetime.now().strftime("%Y-%m-%d")

        form_data = {
            "QUERY": "ACCESOS",
            "DATOSFORM": f"FECHAINI={today}&FECHAFIN={today}",
        }

        headers = {"user-agent": ""}
        response = requests.post(
            f"{self._base_url}/main_servidor.php",
            data=form_data,
            headers=headers,
            cookies=self._cookies,
        )

        try:
            if not response.json()["sesion"]:
                raise Unauthorized()
        except KeyError:
            pass
        except Exception as e:
            raise e

        html_content = response.json()["html"]

        match = re.search(r"tablaReser\s*=\s*(\[.*?\]);", html_content, re.DOTALL)
        if match:
            # Extract the array content
            array_content = match.group(1)
            # Clean and parse the JSON
            try:
                return json.loads(array_content)
            except json.JSONDecodeError:
                raise ParseException("Error parsing JSON")
            except Exception as e:
                raise e


class ParseException(Exception):
    pass


class Unauthorized(Exception):
    pass
