import re
from collections import defaultdict

photos_base_url = 'http://openglidernetwork.wdfiles.com'

heading_pattern = re.compile("""\+\+ (.*) ?\[\[(.*)\n""")
receiver_pattern = re.compile("""\|\| \|\| ?\[\[# (.*)\]\](?:.*) \|\|(.*)\|\|(.*)\|\|(?:.*)\|\|(?:.*)\|\|(.*)\|\|""")
mail_pattern = re.compile(""".*\[\[\[mailto:(.*)(\?.*\| )| *(.*) *\]\]\]""")
photos_pattern = re.compile('\\[\\*(?P<url>[^ \\[\\]]*) (?P<name>[^ \\[\\]]*)\\]')


# TODO:
# - Parse Poland and Slovakia (table scheme differs)
# - Detect hidden stations (like UKELY)
# - Handle contact information of Sebs stations
def parse_contact(raw):
    contact = ""
    mailmatch = re.match(mail_pattern, raw)
    if mailmatch:
        contact = mailmatch.group(1)
    else:
        if "/contact Seb" in raw:
            contact = raw
        else:
            if "UKELY" in raw:
                pass
            contact = raw.replace("&nbsp;", "").replace("[", "").replace("]", "").replace("|", "").strip()
    return contact


def parse_photo_links(raw):
    links = re.findall(photos_pattern, raw)
    photos = []
    if links:
        for link in links:
            if link[0].startswith('/local--files'):
                photos.append('{}/{}'.format(photos_base_url, link[0]))
            else:
                photos.append(link[0])
    return photos


def parse_receiver_list(page):
    # Seperate list by headings (country)
    country = "None"
    data = defaultdict(list)
    for line in page.splitlines(True):
        heading = re.search(heading_pattern, line)
        if heading:
            country = heading.group(1).strip().lower()
        else:
            data[country].append(line)

    # Parse receiver lists
    stations = {}
    for country in data:
        rawstations = re.findall(receiver_pattern, "".join(data[country]))
        for rawstation in rawstations:
            stations[rawstation[0]] = {"description": rawstation[1].replace("&nbsp;", "").strip(),
                                       "photos": parse_photo_links(rawstation[2]),
                                       "contact": parse_contact(rawstation[3]),
                                       "country": country}
    return stations
