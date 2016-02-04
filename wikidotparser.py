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

photos_pattern = re.compile(r'\[\*?(?P<photo_url>[^\ \[\]]*)\ (?P<name>[^\ \[\]]*)\]')

contact_mail_pattern = re.compile(r'\[\[\[mailto:(?P<email>[^?]*)(?:.*)\|(?P<name>.*)\]\]\]')
contact_url_pattern = re.compile(r'\[\[\[(?P<url>http.*)\|(?P<name>.*)\]\]\]')
contact_intern_pattern = re.compile(r"""\[\/contact\ (?P<name0>\S*)
                                        (
                                          \]\ \/\ \[\/contact\ (?P<name1>.*)\] |
                                          \]\ \/\ (?P<name2>.*) |
                                          \]
                                        )""", re.MULTILINE | re.VERBOSE)


def parse_contact(raw):
    contact_infos = {}
    raw = raw.replace("&nbsp;", "")

    match_mail = re.search(contact_mail_pattern, raw)
    match_url = re.search(contact_url_pattern, raw)
    match_intern = re.search(contact_intern_pattern, raw)

    if match_mail:
        # found an email address
        contact = match_mail.group('email')
    elif match_url:
        # found a hyperlink
        contact = match_url.group('url')
    elif match_intern:
        # found a link to the wiki page '/contact'
        contact = ' / '.join(name for name in match_intern.groupdict().values() if (name is not None))
    else:
        name = raw.replace("[", "").replace("]", "").replace("|", "").strip()
        if name:
            # found a name
            contact = name
        else:
            # found nothing
            contact = ''
    return contact.strip()


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

    receivers = []
    # Parse lines
    for country, lines in data.items():
        for line in lines:
            match = re.match(receiver_pattern, line)
            if match:
                receivers.append({'callsign': match.group('aprsname'),
                                 'description': match.group('desc').replace('&nbsp;', '').strip(),
                                 'photos': parse_photo_links(match.group('photos')),
                                 'contact': parse_contact(match.group('contact')),
                                 'country': country})
    return receivers
