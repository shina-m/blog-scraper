import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from os.path import exists
from markdownify import MarkdownConverter
import pickle
from num2words import num2words
import datetime
from collections import OrderedDict

# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)
base_url = "https://nccf.church/Blog.aspx?BlogID="


bobby_posts =  [6, 7, 8, 12, 13, 14, 16, 18, 20, 22, 23, 24, 25, 26, 27, 29, 31, 34, 37, 38, 41, 43, 48, 52, 55, 56, 60, 63, 64, 67, 71, 73, 80, 81, 82, 83, 84, 90, 97, 98, 99, 100, 109, 111, 112, 114, 119, 124, 127, 130, 136, 137, 146, 154, 156, 157, 158, 159, 166, 170, 177, 178, 186, 187, 190, 195, 196, 198, 203, 207, 210, 214, 217, 221]
order = [(13, 1378018800), (14, 1380610800), (16, 1388563200), (18, 1393660800), (20, 1398927600), (22, 1409727600), (23, 1414652400), (24, 1417680000), (25, 1420617600), (26, 1424160000), (27, 1427353200), (29, 1431414000), (31, 1433746800), (34, 1437634800), (37, 1440745200), (38, 1442646000), (41, 1446969600), (43, 1449820800), (48, 1453449600), (52, 1458802800), (55, 1461913200), (56, 1464246000), (60, 1475650800), (63, 1480320000), (64, 1480320000), (67, 1485676800), (71, 1492671600), (73, 1499670000), (80, 1512979200), (81, 1512979200), (82, 1515657600), (83, 1520496000), (84, 1522652400), (90, 1525244400), (97, 1530860400), (98, 1531292400), (99, 1532415600), (100, 1534402800), (6, 1536562800), (7, 1537167600), (8, 1537858800), (109, 1540450800), (111, 1542355200), (112, 1543478400), (114, 1546156800), (119, 1550563200), (124, 1552287600), (127, 1557039600), (130, 1564124400), (136, 1568703600), (137, 1568703600), (12, 1575446400), (146, 1576915200), (154, 1580976000), (156, 1582790400), (159, 1583308800), (158, 1583395200), (157, 1583481600), (166, 1585983600), (170, 1587884400), (177, 1593586800), (178, 1594623600), (186, 1602486000), (187, 1602486000), (190, 1606118400), (195, 1610784000), (196, 1612339200), (198, 1616137200), (203, 1621753200), (207, 1633330800), (210, 1637136000), (214, 1641801600), (217, 1642406400), (221, 1647586800)]

header_template = '''\
---
title: {}
date: {}
url: {}
---
'''

time_dict = {}
# for blog_id in [90]:
for i, t in enumerate(order):
    blog_id = t[0]
    url = "https://nccf.church/Blog.aspx?BlogID={}".format(blog_id)
    pickle_file = "raw_pages/{}.pickle".format(blog_id)
    if exists(pickle_file):
        with open(pickle_file, "rb") as pf:
            page = pickle.load(pf)
    else:
        try:
            page = requests.get(url)
            with open(pickle_file, "wb") as pf:
                pickle.dump(page, pf)
        except:
            continue


    # page = urlopen(url)
    # html_bytes = page.read()
    # html = html_bytes.decode("utf-8")
    # print(html)

    soup = BeautifulSoup(page.content, "html.parser")

    # remove empty tags/h2:
    for x in soup.find_all():
        # fetching text from tag and remove whitespaces
        if len(x.get_text(strip=True)) == 0:
            # Remove empty tag
            x.extract()

    # reduce all h1 tags to h2
    h2_headers = soup.find_all("h1")
    for header in h2_headers:
        header.name = "h3"

    # print(page.content)
    title = soup.find("div", class_="title-top").find("span").text.strip()
    date = soup.find("div", class_="date-top").find("span").text.strip()
    post = soup.find("div", class_="article-text")
    date = soup.find("span", {"id": "ctl00_MainContent_lblDate"}).text.strip()

    post_md = md(post, strip=['blockquote', 'h4'])
    # post_md = post_md.replace(u'\xa0', u' ')
    post_md = re.sub(r'\n\s*\n\s*', '\n\n', post_md).strip()
    post_md = re.sub(r'\s*\xa0\s*', ' ', post_md).strip()
    post_md = re.sub(r'###\s*\n', '### ', post_md).strip()

    # header = header_template.format(title, date, url)
    image_file = "out/images/{}.jpg".format(blog_id)

    if exists(image_file):
        post_md = "![](images/{}.jpg)\n\n".format(blog_id) + post_md

    header = "# Chapter {}\n## {}\n*{}*\n[[link]({})] \n\n".format(
        num2words(i+1).replace('-', ' ').title(),
        title.title(),
        date,
        url,
    )

    post_md = header + post_md

    # post_md.replace('### \n', '###')
    # print(repr(post_md))
    with open("out/{}.md".format(blog_id), "w", encoding='utf-8') as f:
        # f.write(header + post_md + "\n")
        f.write( post_md + "\n")

#     timestamp = int(datetime.datetime.strptime(date, "%b %d, %Y").strftime("%s"))
#     print(timestamp)
#     time_dict[blog_id] = timestamp
# print(sorted(time_dict.items(), key=lambda x:x[1]))



### Compiler

book = ""

for i,_ in order:
    with open("out/{}.md".format(i), "r") as f:
        book += f.read() + "\n\n"


with open("book.md", "w", encoding='utf-8') as f:
    f.write(book)

