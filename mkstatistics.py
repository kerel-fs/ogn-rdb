#!/usr/bin/env python3

import json
from collections import defaultdict
from argparse import ArgumentParser

"""
Generate statistics for receivers.json
"""


def print_stats(stations):
    stat_by_country = defaultdict(dict)
    for s in stations:
        stat_by_country[stations[s]['country']][s] = stations[s]

    for c in stat_by_country:
        print("Found %i stations in %s" % (len(stat_by_country[c]), c))
        for s in stat_by_country[c]:
            print(" - %s" % s)

    print("Parsed %i stations in %i countries." % (len(stations), len(stat_by_country)))


if __name__ == "__main__":
    PARSER = ArgumentParser(description="""Generate statistics of a given receiver-wiki.json.""")

    PARSER.add_argument("--in",
                        metavar="IN_FILE", dest="in_file",
                        default="receivers.json",
                        help="Input file. Default: 'receiver-wiki.json'")

    ARGS = PARSER.parse_args()

    with open(ARGS.in_file) as f:
        receiverdb = json.load(f)

    stations = receiverdb['receivers']
    print_stats(stations)
