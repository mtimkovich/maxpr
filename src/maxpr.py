#!/usr/bin/env python3
import argparse
from datetime import date
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
    for i, player in enumerate(players, 1):
        print('{: >3} {: >30} {: >20}'.format(i, player.tag, player.elo()))

parser = argparse.ArgumentParser(description='Create Elo rankings from smash.gg brackets')
parser.add_argument('file', help="Input file containing brackets to use. Will ignore lines starting with '#'")
parser.add_argument('--html', help='Output to html file')
parser.add_argument('--title', default='[Tournament Name]', help='Name of tournament series')
parser.add_argument('--tag-map', help='JSON file containing mappings from incorrect gamertags to correct gamertags')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
args = parser.parse_args()

tournaments = parse_file(args.file)

tag_mappings = {}
if args.tag_map is not None:
    with open(args.tag_map) as f:
        tag_mappings = json.load(f)['maps']

players = {}
for i, tournament in enumerate(tournaments):
    # TODO: Error checking
    if args.verbose:
        print('Downloading: {}'.format(tournament))
    smash_gg = smash.gg(tournament, tag_mappings)
    smash_gg.calc_elo(players, i)
    recent_tourney = i

# set to remove the duplicates
players_list = sorted(set(players.values()), reverse=True)
# remove inactive players after inactive_count tournaments
inactive_count = 5
players_list = [p for p in players_list
                if recent_tourney - p.last_played <= inactive_count]

if args.html:
    today = date.today().strftime('%Y-%m-%d')
    template = Template(filename=os.path.join('template', 'template.html'))
    output = template.render(players=players_list,
                             title=args.title,
                             date=today)
    with open(args.html, 'w') as html:
        html.write(output)

else:
    print_table(players_list)
