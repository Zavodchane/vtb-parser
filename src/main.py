from src.parsers.parser_yandex_map import parse_yandex_map
from src.timers.timers import timer

import json
import time


@timer
def main():
    """
    Updating the database every 24 hours
    """
    while True:

        data = json.load(open("data/offices.txt", encoding="utf-8"))

        vtb_yandex_data = parse_yandex_map(data=data)

        json.dump(vtb_yandex_data, open("data/update_offices.txt", "w"))

        time.sleep(60 * 60 * 24)


if __name__ == "__main__":
    main()
