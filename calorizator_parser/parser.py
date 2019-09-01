""" Crawler for calorizator site. """
from typing import List, Dict, Union
import json
import time
import random
import requests
from bs4 import BeautifulSoup

CALORIZATOR_URL = "http://www.calorizator.ru/product/all"


class CalorizatorApiError(Exception):
    """ Common Calorizator API error. """


def get_main_content(response: requests.Response):
    """ Function that gets <div id='main-content'>..</div> from the response. """
    soup = BeautifulSoup(response.content)

    return soup.find("div", {"id": "main-content"})


def get_calorizator_pages_amount() -> int:
    """ Returns the amount of pages on the calorizator site. """
    response = requests.get(CALORIZATOR_URL)

    if response.status_code != 200:
        raise CalorizatorApiError("Error while getting calorizator pages amount: {}".format(response.status_code))

    main_content = get_main_content(response)

    pager_last = main_content.find("li", {"class": "pager-last"})

    return int(pager_last.string)


def get_calorizator_page(page_idx: int) -> requests.Response:
    """ Function to get the page from calorizator site. """
    response = requests.get(CALORIZATOR_URL, {"page": page_idx})

    if response.status_code != 200:
        raise CalorizatorApiError("Error while getting calorizator page {}: {}".format(page_idx, response.status_code))

    return response


def parse_calorizator_page(page: requests.Response) -> List[Dict[str, Union[str, float]]]:
    """ Parses the calorizator page and extracts the calories data. """
    main_content = get_main_content(page)

    main_table = None

    for table in main_content.find_all("table"):
        try:
            # Find the first 'tr' entry in 'thead'.
            entries = table.thead.find("tr").find_all("th")[2:]
            # Entries list is expected to be like <li><a>NAME</a></li>.
            entries_names = list(map(lambda x: x.a.string, entries))

            # Check if th entries are expected ones.
            expected = ["Бел, г", "Жир, г", "Угл, г", "Кал, ккал"]
            if entries_names == expected:
                # We found table that we need.
                main_table = table
                break
        except AttributeError:
            # If attributeerror happened, it's not the table we're looking for.
            pass

    if not main_table:
        raise CalorizatorApiError("Not found main table on page {}".format(page))

    result = []
    for entry in main_table.find("tbody").find_all("tr"):
        columns = entry.find_all("td")

        parsed_entry = {
            "name": columns[1].a.string.strip(),
            "protein": columns[2].string.strip(),
            "fat": columns[3].string.strip(),
            "hydrocarbonates": columns[4].string.strip(),
            "calories": columns[5].string.strip(),
        }

        result.append(parsed_entry)

    return result


def get_wait_interval(start, stop) -> float:
    """ Function to choose a random number between start and stop. """
    interval = stop - start

    random_shift = random.random() * interval

    return start + random_shift


def wait():
    """ Function that sleeps for a short period of time to prevent high load of the site. """
    wait_interval = get_wait_interval(1, 3)

    time.sleep(wait_interval)


def main():
    """ Main parser function. """
    page_num = get_calorizator_pages_amount()

    result_entries: List[Dict[str, Union[str, float]]] = []
    for page_idx in range(page_num):
        page = get_calorizator_page(page_idx)
        result_entries += parse_calorizator_page(page)

        wait()

    with open("result.json", "w") as file:
        file.write(json.dumps(result_entries))


if __name__ == "__main__":
    main()
