#!/usr/bin/env python
import smash

smash_gg = smash.gg('get-smashed-at-the-foundry-101')

players = {}
smash_gg.calc_elo(players)

for name, player in sorted(players.items(), key=lambda x: x[1].expose()):
    print name, ':', player.expose()
