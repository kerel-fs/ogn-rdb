#!/usr/bin/env python3

import os.path
import json
from datetime import datetime
from argparse import ArgumentParser

from wikidotparser import parse_receiver_list
from wikidotcrawler import fetch_page

wiki_url = 'http://wiki.glidernet.org/ajax-module-connector.php'
page_ids = {'list-of-receivers': 22120125}


def obfuscate_addresses(receiverdb):
    receivers = receiverdb['receivers']
    for s in receivers:
        if receivers[s]['contact']:
            receivers[s].update({'contact': "%s@..." % (receivers[s]['contact'].split('@')[0])})
    receiverdb.update({'receivers': receivers})
    return receiverdb


if __name__ == "__main__":
    PARSER = ArgumentParser(description="""Fetch list-of-receivers from wiki.glidernet.org
                                           and output it into a (machine-readable) file.""")

    PARSER.add_argument("--out",
                        metavar="OUT_FILE", dest="out_file",
                        default="receivers.json",
                        help="Output file. Default:"
    PARSER.add_argument("--nospam",
                        dest="no_spam",
                        default=False,
                        action="store_true",
                        help="Obfuscate email addresses (truncate addresses after '@').")
    ARGS = PARSER.parse_args()

    print("Fetch {}".format(wiki_url))
    page = fetch_page(wiki_url, page_ids['list-of-receivers'])
    timestamp = datetime.utcnow().replace(microsecond=0)

    print("Parse list-of-receivers")
    receiverdb = {'receivers': parse_receiver_list(page),
                  'timestamp': timestamp.isoformat()}

    if ARGS.no_spam:
        print("Obfuscate email addresses.")
        receiverdb = obfuscate_addresses(receiverdb)

    print("Save to {}".format(ARGS.out_file))
    with open(ARGS.out_file, 'w') as f:
        json.dump(receiverdb, f)
