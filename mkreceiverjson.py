#!/usr/bin/env python3

import os.path
import json
from datetime import datetime
from argparse import ArgumentParser

from wikidotparser import parse_receiver_list


def process_list(page, timestamp):
    receivers = parse_receiver_list(page)

    receiverdb = {'receivers': receivers,
                  'timestamp': timestamp.isoformat()}
    return receiverdb

def obfuscate_addresses(receiverdb):
    receivers = receiverdb['receivers']
    for s in receivers:
        if receivers[s]['contact']:
            receivers[s].update({'contact': "%s@..." % (receivers[s]['contact'].split('@')[0])})
    receiverdb.update({'receivers': receivers})
    return receiverdb

def save_data(receiverdb, out_file):
    with open(out_file, 'w') as f:
        json.dump(receiverdb, f)


if __name__ == "__main__":
    PARSER = ArgumentParser(description="""Fetch receiver-list from wiki.glidernet.org
                                           and write the data into an JSON-file.""")

    PARSER.add_argument("--out","-o",
                        metavar="OUT_FILE", dest="out_file",
                        default="receiver-wiki.json",
                        help="Output file. Default:"
                             "receiver-wiki.json")

    PARSER.add_argument("--in","-i",
                        metavar="IN_FILE", dest="in_file",
                        default="list-of-receivers.wikidot",
                        help="Alternative local input file.")

    PARSER.add_argument("--nospam",
                        dest="no_spam",
                        default=False,
                        action="store_true",
                        help="Obfuscate email addresses (truncate address after '@').")


    ARGS = PARSER.parse_args()

    print("Open page %s from file." % ARGS.in_file)
    with open(ARGS.in_file, 'r') as f:
        page = f.read()
    timestamp = datetime.fromtimestamp(os.path.getmtime(ARGS.in_file)).replace(microsecond=0)

    print("Parse wiki page.")
    receiverdb = process_list(page, timestamp)

    if ARGS.no_spam:
        print("Obfuscate email addresses.")
        receiverdb = obfuscate_addresses(receiverdb)

    print("Save data to %s." % ARGS.out_file)
    save_data(receiverdb, ARGS.out_file)
