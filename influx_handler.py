import influxdb


def initialize_influx(database_name: str):
    """
    Initializes InfluxDB to receive UPS data measurements.
    """
    influx_client = influxdb.InfluxDBClient(host='localhost', port=8086)

    database_list = influx_client.get_list_database()
    if all([database['name'] != database_name for database in database_list]):
        print("Database does not yet exist -- creating one now.")
        influx_client.create_database(database_name)
    else:
        # print("UPS database already exists.")
        pass

    return influx_client


def send_data_to_influx(influx_client, database_name, json_data_array):
    """
    Uses the InfluxDB Python API to send data.
    """
    influx_client.switch_database(database_name)
    bool_response = influx_client.write_points(json_data_array)

    return bool_response


# You can use this to test your InfluxDB/Grafana connection. Comes from: https://www.influxdata.com/blog/getting-started-python-influxdb/

sample_input_json_body = [{
    "measurement": "brushEvents",
    "tags": {
        "user": "Carol",
        "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
    },
    "time": "2018-03-28T8:01:00Z",
    "fields": {
        "duration": 127
    }
}, {
    "measurement": "brushEvents",
    "tags": {
        "user": "Carol",
        "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
    },
    "time": "2018-03-29T8:04:00Z",
    "fields": {
        "duration": 132
    }
}, {
    "measurement": "brushEvents",
    "tags": {
        "user": "Carol",
        "brushId": "6c89f539-71c6-490d-a28d-6c5d84c0ee2f"
    },
    "time": "2018-03-30T8:02:00Z",
    "fields": {
        "duration": 129
    }
}]
