import logging
from config.env import config
from service.scraper_service import ScrapperService
import schedule
import time
from utils.utility import get_sleep_seconds


def main():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Starting spl-access-worker...")
    scrapper_service = ScrapperService(config)

    schedule.every(10).seconds.do(scrapper_service.main_task)

    while True:
        schedule.run_pending()
        time.sleep(1)

        sleep_seconds = get_sleep_seconds()
        if sleep_seconds > 0:
            logging.info(f"Sleeping for {(sleep_seconds / 3600):.2f} hours...")
            time.sleep(sleep_seconds)


if __name__ == "__main__":
    main()
