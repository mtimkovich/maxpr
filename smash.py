#!/usr/bin/env python
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
            if self.prefix.endswith('.') or self.prefix.endswith('|'):
                glue = ' '
            return '{}{}{}'.format(self.prefix, glue, self.gamerTag)

    # Round rating to two decimal places
    def expose(self):
        return round(trueskill.expose(self.rating), 2)


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
        self.id = self.get_id()
        self.entrants = self.get_entrants()
        self.sets = self.get_sets()

    # TODO: get all group ids and loop over them for tournaments with pools
    def get_id(self):
        r = requests.get('{}/event/melee-singles?expand[]=groups'.format(self.url))
        id = r.json()['entities']['groups'][0]['id']
        return id

    def get_entrants(self):
        r = requests.get('{}?expand[]=entrants'.format(self.url))
        entries = r.json()['entities']['player']
        entrants = {}

        for e in entries:
            entrants[int(e['entrantId'])] = Entry(e)

        return entrants

    def get_sets(self):
        phase = self.PHASE_URL.format(self.id)
        r = requests.get('{}?expand[]=sets'.format(phase))
        raw_sets = r.json()['entities']['sets']

        sets = []
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

if __name__ == '__main__':
    g = gg('get-smashed-at-the-foundry-101')

    players = {}
    g.calc_elo(players)

    i = 1
    for player in sorted(players.values(), key=lambda x: x.expose(), reverse=True):
        print '{: >3} {: >30} {: >20}'.format(i, player.name(), player.expose())
        i += 1
