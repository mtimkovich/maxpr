#!/usr/bin/env python3
import pysmash
import trueskill


class Player:
    def __init__(self, tag):
        self.tag = tag
        self.rating = trueskill.Rating()
        self.last_played = 0

    def elo(self):
        return trueskill.expose(self.rating)

    def __lt__(self, other):
        return self.elo() < other.elo()


class gg:
    """
    This should be capitalized, but jokes are more important than style
    """

    def __init__(self, tournament, tag_remap={}):
        self.tag_remap = tag_remap
        self._parse_url(tournament)
        smash = pysmash.SmashGG()
        self.sets = smash.tournament_show_sets(self.tournament, self.event)
        self.entrants = smash.tournament_show_players(self.tournament, self.event)

    def _parse_url(self, tournament_url):
        split = tournament_url.split('/')

        try:
            self.tournament = split[split.index('tournament') + 1]
            self.event = split[split.index('events') + 1]
        except IndexError:
            print('Invalid smash.gg URL: ' + tournament)
            raise

    def _get_tag_from_id(self, id):
        for e in self.entrants:
            if e['entrant_id'] == int(id):
                return e['tag']
        raise ValueError('player id not in entrants list. possible issue with smash.gg?')

    def _get_player_from_id(self, id):
        return self.players[self._get_tag_from_id(id)]

    def _rate_match(self, match):
        """
        Take match dict and update elo for players
        -1 indicates DQ
        """
        if (match['entrant_1_id'] is None or
                match['entrant_2_id'] is None or
                match['winner_id'] is None or
                (match['entrant_1_score'] is not None and
                    match['entrant_1_score'] == -1) or
                (match['entrant_2_score'] is not None and
                    match['entrant_2_score'] == -1)):
            return

        one = self._get_player_from_id(match['entrant_1_id'])
        two = self._get_player_from_id(match['entrant_2_id'])

        if match['entrant_1_id'] == match['winner_id']:
            one.rating, two.rating = trueskill.rate_1vs1(one.rating, two.rating)
        elif match['entrant_2_id'] == match['winner_id']:
            two.rating, one.rating = trueskill.rate_1vs1(two.rating, one.rating)
        else:
            raise ValueError("Winner ID not one of the player's id. smash.gg error?")

    def calc_elo(self, players, tourney_num):
        """
        Calculate elo for every match in tournament in order
        """
        self.players = players
        grand_finals = []

        for match in self.sets:
            for entrant_id in [match['entrant_1_id'], match['entrant_2_id']]:
                tag = self._get_tag_from_id(entrant_id)

                if tag not in players:
                    pl = Player(tag)
                    players[tag] = pl

                    pl.tag = self.tag_remap.get(pl.tag, pl.tag)
                else:
                    pl = players[tag]

                pl.last_played = tourney_num

            # Rate GF match last
            if match['short_round_text'] == 'GF':
                grand_finals.append(match)
            else:
                self._rate_match(match)

        for match in grand_finals:
            self._rate_match(match)
