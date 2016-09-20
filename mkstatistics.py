#!/usr/bin/env python3

import json
from collections import defaultdict
from argparse import ArgumentParser

"""
Generate statistics for receivers.json

Equivalent:
cat receivers.json | jq ".receivers | group_by(.country) | map({(.[0].country): [.[].callsign]})"
"""


def print_stats(all_receivers):
    receivers_by_country = defaultdict(list)
    for receiver in all_receivers:
        receivers_by_country[receiver["country"]].append(receiver)

    for country, receivers in receivers_by_country.items():
        print('Found {} receivers in {}'.format(len(receiver), country))
        for receiver in receivers:
            print(' - {}'.format(receiver["callsign"]))

    print('Found {} receivers in {} countries.'.format(len(all_receivers), len(receivers_by_country)))


if __name__ == "__main__":
    PARSER = ArgumentParser(description="""Generate statistics of a given receiver-wiki.json.""")

    PARSER.add_argument("--in",
                        metavar="IN_FILE", dest="in_file",
                        default="receivers.json",
                        help="Input file. Default: 'receiver-wiki.json'")

    ARGS = PARSER.parse_args()

    with open(ARGS.in_file) as f:
        receiverdb = json.load(f)

    if receiverdb['version'][:3] == "0.2":
        receivers = receiverdb['receivers']
        print_stats(receivers)
    else:
        print("Unsupported receiverlist version ({}).".format(receiverdb['version']))
