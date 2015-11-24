import re
from collections import defaultdict

photos_base_url = 'http://openglidernetwork.wdfiles.com'
# TODO: Fix Poland and Slovkia.

# Known to be broken:
# receiver_pattern = re.compile("""\|\| \|\| ?\[\[# (.*)\]\](?:.*) \|\|(.*)\|\|(.*)\|\|(?:.*)\|\|((?:.*)\|\||)(.*)\|\|""")

# Goal: at least 486 stations in 22 countries (November 2015)
heading_pattern = re.compile("""\+\+ (.*) ?\[\[(.*)\n""")
receiver_pattern = re.compile("""\|\| \|\| ?\[\[# (.*)\]\](?:.*) \|\|(.*)\|\|(.*)\|\|(?:.*)\|\|(?:.*)\|\|(.*)\|\|""")
mail_pattern = re.compile(""".*\[\[\[mailto:(.*)(\?.*\| )| *(.*) *\]\]\]""")
photos_pattern = re.compile('\\[\\*(?P<url>[^ \\[\\]]*) (?P<name>[^ \\[\\]]*)\\]')

def parse_contact(raw):
    contact = ""
    mailmatch = re.match(mail_pattern, raw)
    if mailmatch:
        contact = mailmatch.group(1)
    else:
        if "/contact Seb" in raw:
            # TODO: Catch Sebs stations
            contact = raw
        else:
            if "UKELY" in raw:
                # TODO: Catch this hidden stations
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
