#!/usr/bin/env python
# encoding: utf-8
import argparse
from mako.template import Template
import smash


def parse_file(file):
    tournaments = []
    with open(args.file) as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                tournaments.append(line)

    return tournaments


def print_table(players):
    i = 1
    for player in sorted(players.values(), key=lambda x: x.elo(), reverse=True):
        print '{: >3} {: >30} {: >20}'.format(i, player.name(), player.elo())
        i += 1

parser = argparse.ArgumentParser(description='Create Elo rankings from smash.gg brackets')
parser.add_argument('file', help="Input file containing tournaments to use. Will ignore lines starting with '#'")
parser.add_argument('--html', action='store_true', help='Output html file')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
args = parser.parse_args()

tournaments = parse_file(args.file)

players = {}
for tournament in tournaments:
    # TODO: Error checking
    if args.verbose:
        print 'Downloading: {}'.format(tournament)
    smash_gg = smash.gg(tournament)
    smash_gg.calc_elo(players)

if args.html:
    template = Template(filename='template.html', default_filters=['decode.utf8'], 
                        input_encoding='utf-8', output_encoding='utf-8')
    print template.render(players=sorted(players.values(), key=lambda x: x.elo(), reverse=True))
else:
    print_table(players)
