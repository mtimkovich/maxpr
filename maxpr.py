#!/usr/bin/env python
import smash

smash_gg = smash.gg('get-smashed-at-the-foundry-101')

players = {}
smash_gg.calc_elo(players)

i = 1
for name, player in sorted(players.items(), key=lambda x: x[1].expose(), reverse=True):
    print '{: >3} {: >20} {: >20}'.format(i, name, player.expose())
    i += 1
