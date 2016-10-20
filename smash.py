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
        for _ in range(self.entrant1Score):
            one.rating, two.rating = trueskill.rate_1vs1(one.rating, two.rating)
        for _ in range(self.entrant2Score):
            two.rating, one.rating = trueskill.rate_1vs1(two.rating, one.rating)

        return one, two


class Player:
    def __init__(self, name):
        self.name = name
        self.rating = trueskill.Rating()

    # Round rating to two decimal places
    def expose(self):
        return round(trueskill.expose(self.rating), 2)


# This should be capitalized, but jokes are more important than style
class gg:
    def __init__(self, tournament):
        self.BASE_URL = 'https://api.smash.gg/tournament/{}/event/melee-singles'
        self.PHASE_URL = 'https://api.smash.gg/phase_group/{}'

        self.tournament = tournament
        self.url = self.BASE_URL.format(self.tournament)
        self.request = requests.get('{}?expand[]=groups&expand[]=entrants'.format(self.url)).json()
        self.id = self.get_id()
        self.entrants = self.get_entrants()
        self.sets = self.get_sets()

    def get_id(self):
        id = self.request['entities']['groups'][0]['id']
        return id

    def get_entrants(self):
        entries = self.request['entities']['entrants']
        entrants = {}

        for e in entries:
            entrants[e['id']] = e['name']

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
            if s.entrant1 not in players:
                players[s.entrant1] = Player(s.entrant1)
            if s.entrant2 not in players:
                players[s.entrant2] = Player(s.entrant2)

            one = players[s.entrant1]
            two = players[s.entrant2]

            one, two = s.rate(one, two)

if __name__ == '__main__':
    g = gg('get-smashed-at-the-foundry-101')

    players = {}
    g.calc_elo(players)

    i = 1
    for name, player in sorted(players.items(), key=lambda x: x[1].expose(), reverse=True):
        print '{: >3} {: >20} {: >20}'.format(i, name, player.expose())
        i += 1
