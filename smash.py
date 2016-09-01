#!/usr/bin/env python
import requests
import trueskill


class Set:
    def __init__(self, match):
        self.entrant1 = match['entrant1Id']
        self.entrant2 = match['entrant2Id']
        self.winner = match['winnerId']
        self.entrant1Score = match['entrant1Score']
        self.entrant2Score = match['entrant2Score']

    # Calculate the rating for each game in the set
    def rate(self, one, two):
        for _ in range(self.entrant1Score):
            one.rating, two.rating = trueskill.rate_1vs1(one.rating, two.rating)
        for _ in range(self.entrant2Score):
            two.rating, one.rating = trueskill.rate_1vs1(two.rating, one.rating)

        return one, two


# TODO: Map ids to player tags
class Player:
    def __init__(self, id):
        self.id = 0
        self.rating = trueskill.Rating()

    def expose(self):
        return trueskill.expose(self.rating)


# This should be capitalized, but jokes are more important than style
class gg:
    def __init__(self, tournament):
        self.tournament = tournament
        r = requests.get('https://api.smash.gg/tournament/{}/event/melee-singles?expand[0]=groups&expand[1]=phase'.format(self.tournament))
        self.id = r.json()['entities']['groups'][0]['id']

        r = requests.get('https://api.smash.gg/phase_group/{}?expand[]=sets'.format(self.id))
        raw_sets = r.json()['entities']['sets']

        self.sets = []
        for s in raw_sets:
            if s['entrant1Id'] is None or s['entrant2Id'] is None:
                continue
            self.sets.append(Set(s))


if __name__ == '__main__':
    g = gg('get-smashed-at-the-foundry-101')

    # TODO: Move this to method
    players = {}

    for s in g.sets:
        if s.entrant1 not in players:
            players[s.entrant1] = Player(s.entrant1)
        if s.entrant2 not in players:
            players[s.entrant2] = Player(s.entrant2)

        one = players[s.entrant1]
        two = players[s.entrant2]

        one, two = s.rate(one, two)

    for id, player in sorted(players.items(), key=lambda x: x[1].expose()):
        print id, ':', trueskill.expose(player.rating)
