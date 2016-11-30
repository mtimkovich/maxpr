#!/usr/bin/env python3
import argparse
import json
from mako.template import Template
import os
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
    for i, player in enumerate(players):
        print('{: >3} {: >30} {: >20}'.format(i+1, player.name(), player.elo()))

parser = argparse.ArgumentParser(description='Create Elo rankings from smash.gg brackets')
parser.add_argument('file', help="Input file containing tournaments to use. Will ignore lines starting with '#'")
parser.add_argument('--html', action='store_true', help='Output html file')
parser.add_argument('--tag-map', help='JSON file containing mappings from incorrect gamertags to correct gamertags')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
args = parser.parse_args()

tournaments = parse_file(args.file)

tag_mappings = {}
if args.tag_map is not None:
    with open(args.tag_map) as f:
        tag_mappings = json.load(f)['maps']

players = {}
date = None
for tournament in tournaments:
    # TODO: Error checking
    if args.verbose:
        print('Downloading: {}'.format(tournament))
    smash_gg = smash.gg(tournament, tag_mappings)
    smash_gg.calc_elo(players)
    date = smash_gg.date

# set to remove the duplicates
players_list = sorted(set(players.values()), reverse=True)

if args.html:
    template = Template(filename=os.path.join('template', 'template.html'))
    print(template.render(players=players_list,
                          date=date))
else:
    print_table(players_list)
