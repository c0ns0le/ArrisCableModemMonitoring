import bs4

# read html file in as string
# pass it to BS parser

with open("html/status_page.html", "r") as status_html:
    status_html_string = ''.join([line.replace('\n', '') for line in status_html.readlines()])




beautifulsoup = bs4.BeautifulSoup(status_html_string)

status_table = beautifulsoup.find_all("table", attrs={'class' : 'simpleTable'})

# there's 2 "simple_tables", the one we want is the 2nd one

print(status_table)