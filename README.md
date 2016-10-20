MaxPR for Get Smashed at the Foundry
====================================

Generates an Elo rating for all players in the Get Smashed at the Foundry from the smash.gg brackets using [TrueSkill](http://trueskill.org/).
Ratings go from 0 to 50.

Should hopefully be general enough to work with other smash.gg tournaments as well.

Usage
-----

`maxpr.py` takes one argument, which is a file with all tournaments to scrape from, with each tournament on a separate line.
You can get the tournament id from the smash.gg URL e.g. for https://smash.gg/tournament/get-smashed-at-the-foundry-101/events,
the tournament id is `get-smashed-at-the-foundry-101`. Lines starting with an '#' will be ignored.

