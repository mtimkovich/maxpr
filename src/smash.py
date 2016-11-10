#!/usr/bin/env python
from datetime import datetime
import requests
import trueskill


class Set:
    def __init__(self, match, entrants):
        self.entrant1 = entrants[match['entrant1Id']]
        self.entrant2 = entrants[match['entrant2Id']]
        self.entrant1Score = match['entrant1Score']
        self.entrant2Score = match['entrant2Score']

    # Calculate the rating for each game in the set
    def rate(self, one, two):
        if self.entrant1Score >= 0 and self.entrant2Score >= 0:
            for _ in range(self.entrant1Score):
                one.rating, two.rating = trueskill.rate_1vs1(one.rating, two.rating)
            for _ in range(self.entrant2Score):
                two.rating, one.rating = trueskill.rate_1vs1(two.rating, one.rating)

        return one, two


class Player:
    def __init__(self, entry):
        self.gamerTag = entry.gamerTag
        self.prefix = entry.prefix
        self.id = entry.id
        self.rating = trueskill.Rating()

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


class Entry:
    def __init__(self, entry):
        self.gamerTag = entry['gamerTag'].encode('utf-8')
        self.prefix = entry['prefix']
        if self.prefix is not None:
            self.prefix = self.prefix.encode('utf-8')
        self.id = entry['id']
        self.entrantId = entry['entrantId']


# This should be capitalized, but jokes are more important than style
class gg:
    def __init__(self, tournament):
        self.BASE_URL = 'https://api.smash.gg/tournament/{}'
        self.PHASE_URL = 'https://api.smash.gg/phase_group/{}'

        self.tournament = tournament
        self.url = self.BASE_URL.format(self.tournament)
        self.date = None
        self.ids = self.get_ids()
        self.entrants = self.get_entrants()
        self.sets = self.get_sets()

    def get_ids(self):
        r = requests.get('{}/event/melee-singles?expand[]=groups'.format(self.url))

        self.date = r.json()['entities']['event']['startAt']
        self.date = datetime.fromtimestamp(self.date).strftime('%Y-%m-%d')
        
        return [i['id'] for i in r.json()['entities']['groups']]

    def get_entrants(self):
        r = requests.get('{}?expand[]=entrants'.format(self.url))
        entries = r.json()['entities']['player']
        entrants = {}

        for e in entries:
            entrants[int(e['entrantId'])] = Entry(e)

        return entrants

    def get_sets(self):
        sets = []

        for id in self.ids:
            phase = self.PHASE_URL.format(id)
            r = requests.get('{}?expand[]=sets'.format(phase))
            raw_sets = r.json()['entities']['sets']

            for s in raw_sets:
                if s['entrant1Id'] is not None and s['entrant2Id'] is not None:
                    sets.append(Set(s, self.entrants))

        return sets

    def calc_elo(self, players):
        for s in self.sets:
            if s.entrant1.id not in players:
                players[s.entrant1.id] = Player(s.entrant1)
            if s.entrant2.id not in players:
                players[s.entrant2.id] = Player(s.entrant2)

            one = players[s.entrant1.id]
            two = players[s.entrant2.id]

            one, two = s.rate(one, two)
