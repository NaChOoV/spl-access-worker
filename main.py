import logging
from config.env import config
from service.scraper_service import ScrapperService
import schedule
import time


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

        check_sleep_time()


def check_sleep_time():
    current_hour = time.localtime().tm_hour
    current_minute = time.localtime().tm_min
    current_second = time.localtime().tm_sec

    if current_hour >= 23 or current_hour < 6:
        if current_hour >= 23:
            next_wakeup_hour = 30.5  # 6.5 + 24
        else:
            next_wakeup_hour = 6.5
        time_left = (
            (next_wakeup_hour - current_hour) * 3600
            - current_minute * 60
            - current_second
        )

        time_left_hours = time_left / 3600
        logging.info(f"Sleeping for {time_left_hours:.2f} hours")
        time.sleep(time_left)


if __name__ == "__main__":
    main()
