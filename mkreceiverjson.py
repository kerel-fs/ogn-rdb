#!/usr/bin/env python3

import os.path
import json
from datetime import datetime
from argparse import ArgumentParser

from wikidotparser import parse_receiver_list
from wikidotcrawler import fetch_page

wiki_url = 'http://wiki.glidernet.org/ajax-module-connector.php'
page_ids = {'list-of-receivers': 22120125,
            'list-of-receivers-french' : 45174721,
            'list-of-receivers-german' : 45177548,
            'list-of-receivers-uk' : 45177553}

RECEIVERLIST_VERSION = '0.2.1'


if __name__ == "__main__":
    PARSER = ArgumentParser(description="""Fetch list-of-receivers from wiki.glidernet.org
                                           and output it into a (machine-readable) file.""")

    PARSER.add_argument("--out",
                        metavar="OUT_FILE", dest="out_file",
                        default="receivers.json",
                        help="Output file. Default:"
                             "receivers.json")
    PARSER.add_argument("--obfuscate",
                        dest="obfuscate",
                        default=False,
                        action="store_true",
                        help="Obfuscate email addresses (truncate addresses after '@').")
    ARGS = PARSER.parse_args()

    print("Fetch and parse lists of receivers")
    receivers = []
    for page_id in page_ids.values():
        page = fetch_page(wiki_url, page_id)
        receivers += parse_receiver_list(page)

    timestamp = datetime.utcnow().replace(microsecond=0)

    receiverdb = {'version': RECEIVERLIST_VERSION,
                  'receivers': receivers,
                  'timestamp': timestamp.isoformat()}

    if ARGS.obfuscate:
        print("Obfuscate email addresses")
        for receiver in receiverdb['receivers']:
            receiver.update({'email': ''})


    print("Save to {}".format(ARGS.out_file))
    with open(ARGS.out_file, 'w') as f:
        json.dump(receiverdb, f)
