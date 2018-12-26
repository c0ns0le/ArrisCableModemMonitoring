import bs4

# read html file in as string
# pass it to BS parser


def extract_status_data(status_page_html=None):


    with open("html/status_page.html", "r") as status_html:
        status_html_string = ''.join([line.replace('\n', '') for line in status_html.readlines()])


    beautifulsoup = bs4.BeautifulSoup(status_html_string)

    status_table = beautifulsoup.find_all("table", attrs={'class' : 'simpleTable'})


def extract_product_information(product_information_page_html=None):
    pass



def construct_status_dict_from_table_html(table_html):
    """
    Given the html for all tables on the status page, convert them to a dictionary object
    """

def parse_downstream_channel_info(downstream_table_html):
    pass


def parse_upstream_channel_info(upstream_table_html):
    pass


def parse_startup_procedure(startup_table_html):
    pass

