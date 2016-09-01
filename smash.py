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
    sets = g.sets

    print sets[0].entrant1
