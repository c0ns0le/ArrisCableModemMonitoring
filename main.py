import time

import influx_handler
import logstash_handler
import retriever

if __name__ == '__main__':
    while (True):
        status_page_html = retriever.make_page_request()

        status_tables = retriever.extract_status_data(status_page_html)

        downstream_status = retriever.construct_list_from_table_html(status_tables[1])

        upstream_status = retriever.construct_list_from_table_html(status_tables[2])

        downstream_influx_ready_array = retriever.create_influx_ready_array(downstream_status, "downstream")

        upstream_influx_ready_array = retriever.create_influx_ready_array(upstream_status, "upstream")

        client = influx_handler.initialize_influx("arris")

        response_ds = influx_handler.send_data_to_influx(client, "arris", downstream_influx_ready_array)

        response_us = influx_handler.send_data_to_influx(client, "arris", upstream_influx_ready_array)

        if response_ds == True and response_us == True:
            print("Success")

        else:
            print("Failure")

        time.sleep(2)

        resp = logstash_handler.write_to_logstash("Finished one iteration", "warning")
