import datetime
import re
import socket
import typing

import bs4
import requests


# TODO: Extract the IP address of the cable-modem to be a parameter passed through the command line
def make_page_request(url: str = "http://192.168.100.1") -> str:
    """
    Makes a GET request to a specified URL and then returns the HTML of that page as a string
    :param url:
    :return:
    """
    page = requests.get(url)
    return page.content


def extract_table_data(status_html_string: str) -> typing.List:
    """
    Parses a table in HTML form into a list of lists, where each inner list represents a row in that table.
    :param status_html_string:
    :return:
    """
    beautifulsoup = bs4.BeautifulSoup(status_html_string, "html.parser")

    status_table = beautifulsoup.find_all("table", attrs={'class' : 'simpleTable'})

    return status_table

def construct_list_from_table_html(table_html: str) -> typing.List:
    data = []
    rows = table_html.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [el.text.strip() for el in cols]
        data.append([element for element in cols if element])

    return data


def parse_event_log(event_log_list) -> typing.List:
    """
    Parses the event log taken in as a list -- mostly timestamp conversions and removing non-numeric values from the priority list
    :param event_log_list:
    :return: A list where all timestamps are replaced with UTC timestamps, and priority level is integer-type only
    """
    parsed_event_log_list = []
    for row_number, row_data in enumerate(event_log_list[1:]):  # skip the header
        parsed_event_log_element = []
        # TODO : Change this to a list comprehension
        if len(row_data) != 3:
            continue

        raw_time, raw_priority, description = row_data

        if raw_time == "Time Not Established":
            first_time_stamp = datetime.datetime.fromtimestamp(0).strftime('%Y-%m-%d %H:%M:%S')
            parsed_event_log_element.append(first_time_stamp)

        else:
            parsed_timestamp = datetime.datetime.strptime(raw_time, '%a %b %d %H:%M:%S %Y').strftime(
                "%Y-%m-%d %H:%M:%S")
            parsed_event_log_element.append(parsed_timestamp)

        priority_level = re.sub('[^[0-9]', '', raw_priority)

        parsed_event_log_element.append(priority_level)

        # raw_priority = priority_level

        parsed_event_log_element.append(description)

        parsed_event_log_list.append(parsed_event_log_element)

    return parsed_event_log_list




def create_influx_ready_array(table_data: typing.List, direction: str) -> typing.List:
    """
    Given a list of lists representing the table data, this functions converts them to the standard array of JSON objects that InfluxDB requires
    :param table_data:
    :return:
    """
    measurements_array = []  # array of dicts
    rows_list = table_data[1:]
    column_headers_list = rows_list[0]
    number_of_channels = len(rows_list) - 1
    for channel_row_number, channel_row_data in enumerate(rows_list[1:]):
        # start at column #2, first column only contains ID data
        for value_index, value_to_report in enumerate(channel_row_data):
            if value_index in range(0, 4):
                # The values in the 0th-3rd columns aren't numeric
                continue

            measurement_dict = {}
            # For some reason, Grafana doesn't play nice with using spaces in measurement keys?
            measurement_dict["measurement"] = column_headers_list[value_index].replace(" ", "_")

            measurement_dict["tags"] = {"host": socket.gethostname(),
                                        "channel_direction": str(direction),
                                        "channel_id": channel_row_data[3]}

            measurement_dict["fields"] = {
                "value": float(re.sub('[^[0-9]', '', value_to_report))}

            measurement_dict["time"] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

            measurements_array.append(measurement_dict)

    return measurements_array