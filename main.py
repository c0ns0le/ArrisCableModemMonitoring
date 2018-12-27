import influx_handler
import retriever

if __name__ == '__main__':
    while (True):
        status_page_html = retriever.make_page_request()

        status_tables = retriever.extract_status_data(status_page_html)

        downstream_status = retriever.construct_list_from_table_html(status_tables[1])

        influx_ready_array = retriever.create_influx_ready_array(downstream_status, "downstream")

        client = influx_handler.initialize_influx("arris")

        response = influx_handler.send_data_to_influx(client, "arris", influx_ready_array)

        if response == True:
            print("Success")

        else:
            print("Failure")

    time.sleep(2)
