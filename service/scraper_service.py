import logging
from service.source_service import SourceService, Unauthorized
from service.transformer_service import TransformerService
from service.access_service import AccessService


class ScrapperService:
    def __init__(self, config: dict):
        self._config: dict = config
        self._logger = logging.getLogger(self.__class__.__name__)
        self._source_service = SourceService(config)
        self._access_service = AccessService(config)

        self._source_service.login()

    def main_task(self):
        try:
            results: list[dict] = self.get_today_access()
            access = [
                TransformerService.transform_response_access_to_spl_access(result)
                for result in results
            ]

            self._access_service.send_access(access)
            self._logger.info("Access extracted and sended with success.")

        except Exception as e:
            self._logger.error(f"Error on main task: {e}")

    def get_today_access(self):
        try:
            response = self._source_service.get_today_access()

            return response
        except Unauthorized:
            self._logger.info("Expired session, login again")
            self._source_service.login()

            return self.get_today_access()
        except Exception as e:
            raise e
