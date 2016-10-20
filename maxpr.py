#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import smash


def parse_file(file):
    tournaments = []
    with open(args.file) as f:
        for line in f:
            line = line.rstrip()
            if not line.startswith('#'):
                tournaments.append(line)

    return tournaments

parser = argparse.ArgumentParser(description='Create Elo rankings from smash.gg brackets')
parser.add_argument('file', help="Input file containing tournaments to use. Will ignore lines starting with '#'")
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
args = parser.parse_args()

tournaments = parse_file(args.file)

players = {}
i = 0
for tournament in tournaments:
    # TODO: Error checking
    if args.verbose:
        print 'Downloading: {}'.format(tournament)
    smash_gg = smash.gg(tournament)
    smash_gg.calc_elo(players)

    i += 1

    if i >= 2:
        break

i = 1
for name, player in sorted(players.items(), key=lambda x: x[1].expose(), reverse=True):
    print '{: >3} {: >20} {: >20}'.format(i, name, player.expose())
    i += 1
