import re
from collections import defaultdict

photos_base_url = 'http://openglidernetwork.wdfiles.com'

heading_pattern = re.compile(r'\+\+ (?P<text>.*) ?\[\[(?P<tag>.*)\n')
receiver_pattern = re.compile(r"""\|\|\ \|\|\ ?\[\[\#\ (?P<aprsname>.*)\]\](?:.*)
                                  \|\|(?P<desc>.*)
                                  \|\|(?P<photos>.*)
                                  \|\|(?:.*)
                                  \|\|(?P<contact>.*)\|\|""", re.MULTILINE | re.VERBOSE)

wikidot_link_pattern = re.compile(r"\[\*?([^\[\]\ ]*)\ ([^\[\]]*)\]")

photos_pattern = re.compile(r'\[\*?(?P<photo_url>[^\ \[\]]*)\ (?P<name>[^\ \[\]]*)\]')
image_url_pattern = re.compile(r".*\.(jpg|png|gif)$", re.IGNORECASE)

contact_mail_pattern = re.compile(r'\[\[\[mailto:(?P<email>[^?]*)(?:.*)\|\ *(?P<name>.*)\]\]\]')
contact_url_pattern = re.compile(r'\[\[\[(?P<url>http.*)\|(?P<name>.*)\]\]\]')
contact_intern_pattern = re.compile(r"""\[\/contact\ (?P<name0>\S*)
                                        (
                                          \]\ \/\ \[\/contact\ (?P<name1>.*)\] |
                                          \]\ \/\ (?P<name2>.*) |
                                          \]
                                        )""", re.MULTILINE | re.VERBOSE)


def parse_description_links(text):
    links = []
    for link in re.finditer(wikidot_link_pattern, text):
        links.append({'rel': link.group(2), 'href': link.group(1)})
        text = text.replace(link.group(0),link.group(2),1)
    return text, links


def parse_contact(raw):
    contact_details = {'name': '', 'email': ''}
    links = []

    match_mail = re.search(contact_mail_pattern, raw)
    match_url = re.search(contact_url_pattern, raw)
    match_intern = re.search(contact_intern_pattern, raw)

    if match_mail:
        # found an email address
        contact_details = {'name': match_mail.group('name'),
                           'email': match_mail.group('email')}
    elif match_url:
        # found a hyperlink
        links.append({'ref': 'contact', 'href': match_url.group('url')})
    elif match_intern:
        # found a link to the wiki page '/contact'
        contact_details = {'name': ' / '.join(name for name in match_intern.groupdict().values() if (name is not None)), 'email': ''}
    else:
        name = raw.replace("[", "").replace("]", "").replace("|", "").strip()
        if name:
            # found a name
            contact_details = {'name': name, 'email': ''}
        else:
            # found nothing
            pass
    return contact_details, links


def parse_photo_links(raw):
    photos = []
    links = []
    for link in re.finditer(photos_pattern, raw):
        if link.group('photo_url').startswith('/local--files'):
            photos.append('{}/{}'.format(photos_base_url, link.group('photo_url')))
        else:
            if re.match(image_url_pattern, link.group('photo_url')):
                photos.append(link.group('photo_url'))
            else:
                links.append({'href': link.group('photo_url'), 'rel': link.group('name')})
    return photos, links


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
            line = line.replace("&nbsp;", "").replace("&amp;", '&').replace("&quot;", '"')
            match = re.match(receiver_pattern, line)
            if match:
                description, desc_links = parse_description_links(match.group('desc').strip())
                photos, photo_links = parse_photo_links(match.group('photos'))
                contact_details, contact_links = parse_contact(match.group('contact'))
                receivers.append({'callsign': match.group('aprsname'),
                                 'description': description,
                                 'photos': photos,
                                 'links': desc_links + photo_links + contact_links,
                                 'contact': contact_details['name'],
                                 'email': contact_details['email'],
                                 'country': country})
    return receivers
