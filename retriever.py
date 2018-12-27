import datetime
import re
import socket
import typing

import bs4
import requests


# read html file in as string
# pass it to BS parser

def make_page_request(url: str = "http://192.168.100.1") -> str:
    page = requests.get(url)
    return page.content


def extract_status_data(status_html_string: str) -> typing.List:
    # with open("html/status_page.html", "r") as status_html:
    #     status_html_string = ''.join([line.replace('\n', '') for line in status_html.readlines()])

    beautifulsoup = bs4.BeautifulSoup(status_html_string, "html.parser")

    status_table = beautifulsoup.find_all("table", attrs={'class' : 'simpleTable'})

    return status_table


def construct_list_from_table_html(table_html: str) -> typing.List:
    """
    Given the html for all tables on the status page, convert them to a list object for easy parsing
    """

    data = []
    rows = table_html.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [el.text.strip() for el in cols]
        data.append([element for element in cols if element])

    return data


def create_influx_ready_array(table_data: typing.List, direction: str) -> typing.List:
    """
    A list of lists, where each inner list represents a row in the table
    :param table_data:
    :return:
    """
    measurements_array = []  # array of dicts
    rows_list = table_data[1:]
    column_headers_list = rows_list[0]
    number_of_channels = len(rows_list) - 1
    for channel_row_number, channel_row_data in enumerate(rows_list[1:]):
        # start at column #2
        for value_index, value_to_report in enumerate(channel_row_data):
            if value_index == 3 or value_index == 0:  # redundant to make a measurement on the channel id or channel itself
                continue

            if value_index == 1 or value_index == 2:
                continue

            measurement_dict = {}
            # get the "key" for the measurement name
            measurement_dict["measurement"] = column_headers_list[value_index].replace(" ", "_")

            # measurement_dict["tags"] = {}
            # measurement_dict["tags"] = socket.gethostname()
            # import pdb; pdb.set_trace()
            # measurement_dict["tags"]["channel_direction"] +=  str(direction)
            # measurement_dict["tags"]["channel_id"] = channel_row_data[3]

            measurement_dict["tags"] = {"host": socket.gethostname(),
                                        "channel_direction": str(direction),
                                        "channel_id": channel_row_data[3]}

            measurement_dict["fields"] = {
                "value": float(re.sub('[^[0-9]', '', value_to_report))}

            measurement_dict["time"] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            # import pdb; pdb.set_trace()

            measurements_array.append(measurement_dict)

    return measurements_array
