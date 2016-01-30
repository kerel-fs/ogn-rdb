import re
from collections import defaultdict

photos_base_url = 'http://openglidernetwork.wdfiles.com'

heading_pattern = re.compile(r'\+\+ (?P<text>.*) ?\[\[(?P<tag>.*)\n')
receiver_pattern = re.compile(r"""\|\|\ \|\|\ ?\[\[\#\ (?P<aprsname>.*)\]\](?:.*)
                                  \|\|(?P<desc>.*)
                                  \|\|(?P<photos>.*)
                                  \|\|(?:.*)
                                  \|\|(?:.*)
                                  \|\|(?P<contact>.*)\|\|""", re.MULTILINE | re.VERBOSE)
mail_pattern = re.compile(""".*\[\[\[mailto:(.*)(\?.*\| )| *(.*) *\]\]\]""")

photos_pattern = re.compile(r'\[\*(?P<photo_url>[^ \[\]]*) (?P<name>[^ \[\]]*)\]')


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
    photos = []
    for link in re.finditer(photos_pattern, raw):
        if link.group('photo_url').startswith('/local--files'):
            photos.append('{}/{}'.format(photos_base_url, link.group('photo_url')))
        else:
            photos.append(link.group('photo_url'))
    return photos


def parse_receiver_list(page):
    country = 'None'
    data = defaultdict(list)

    # Seperate lines by heading (country)
    for line in page.splitlines(True):
        heading = re.search(heading_pattern, line)
        if heading:
            country = heading.group('text').strip().lower()
        else:
            data[country].append(line)

    stations = {}
    # Parse lines
    for country, lines in data.items():
        for line in lines:
            match = re.match(receiver_pattern, line)
            if match:
                stations[match.group('aprsname')] = {'description': match.group('desc').replace('&nbsp;', '').strip(),
                                                     'photos': parse_photo_links(match.group('photos')),
                                                     'contact': parse_contact(match.group('contact'), match.group('aprsname')),
                                                     'country': country}
    return stations
