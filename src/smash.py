#!/usr/bin/env python3
from datetime import datetime
import pysmash
import re
import requests
import trueskill


class Set:
    def __init__(self, match, entrants):
        self.entrant1 = entrants.get(match.get('entrant1Id', None), None)
        self.entrant2 = entrants.get(match.get('entrant2Id', None), None)
        self.entrant1Score = match['entrant1Score']
        self.entrant2Score = match['entrant2Score']

    # Calculate the rating for each game in the set
    def rate(self, one, two):
        if (self.entrant1Score is None or
                self.entrant2Score is None or
                self.entrant1Score < 0 or
                self.entrant2Score < 0):
            return

        if self.entrant1Score > self.entrant2Score:
            one.rating, two.rating = trueskill.rate_1vs1(one.rating, two.rating)
        else:
            two.rating, one.rating = trueskill.rate_1vs1(two.rating, one.rating)


class Player:
    def __init__(self, entry):
        self.gamerTag = entry.gamerTag
        self.prefix = entry.prefix
        self.id = entry.id
        self.rating = trueskill.Rating()
        self.last_played = 0

    def name(self):
        if not self.prefix:
            return self.gamerTag
        else:
            glue = ' | '
            if self.prefix.endswith('.'):
                glue = ''
            elif self.prefix.endswith('|'):
                glue = ' '
            return '{}{}{}'.format(self.prefix, glue, self.gamerTag)

    def elo(self):
        return trueskill.expose(self.rating)

    def __lt__(self, other):
        return self.elo() < other.elo()


class Entry:
    def __init__(self, entry):
        self.gamerTag = entry['gamerTag']
        self.prefix = entry['prefix']
        self.id = entry['id']
        self.entrantId = entry['entrantId']


# This should be capitalized, but jokes are more important than style
class gg:
    def __init__(self, tournament, tag_remap={}):
        tournament = 'https://smash.gg/tournament/norcal-dogfight-feb-2018/events/dragon-ball-fighterz-singles-5-00-pm/brackets/205410'
        self._parse_url(tournament)
        self.ids = self._get_ids()
        self.entrants = self._get_entrants()
        self.sets = self._get_sets()

    def _parse_url(self, tournament_url):
        split = tournament_url.split('/')

        try:
            self.tournament = split.index('tournament') + 1
            self.event = split.index('events') + 1
        except IndexError:
            print('Invalid smash.gg url: {}'.format(tournament))

    def _get_ids(self):
        pass

    def _get_entrants(self):
        pass

    def _get_sets(self):
        pass

    def calc_elo(self, players, tourney_num):
        for s in self.sets:
            entrants = []

            for e in [s.entrant1, s.entrant2]:
                if e.id not in players:
                    pl = Player(e)
                    players[e.id] = pl

                    pl.gamerTag = self.tag_remap.get(pl.gamerTag, pl.gamerTag)

                    # if name doesn't exist
                    if pl.gamerTag not in players:
                        players[pl.gamerTag] = pl
                    else:
                        pl = players[pl.gamerTag]
                        del players[e.id]
                else:
                    pl = players[e.id]

                pl.last_played = tourney_num
                entrants.append(pl)

            s.rate(entrants[0], entrants[1])
