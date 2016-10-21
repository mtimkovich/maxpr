MaxPR for Get Smashed at the Foundry
====================================

Generates an Elo rating for all players who have competed at the Get Smashed at the Foundry using the [smash.gg][1] brackets.
The Elo is calculated using using [TrueSkill][2].
Ratings go from 0 to 50. This covers all singles Foundry tournaments since July 4th, 2016.

This program should hopefully be general enough to work with other [smash.gg][1] tournaments as well.

Dependencies
------------

- [Mako][3]
- [TrueSkill][2]

Usage
-----

`maxpr.py` takes one argument, which is a file with all tournaments to scrape from, with each tournament on a separate line.
You can get the tournament id from the smash.gg URL e.g. for https://smash.gg/tournament/get-smashed-at-the-foundry-101/events,
the tournament id is `get-smashed-at-the-foundry-101`. Lines starting with a '#' will be ignored.

The `--html` flag can be given to generate the html page.

[1]: http://smash.gg
[2]: http://trueskill.org
[3]: http://www.makotemplates.org
