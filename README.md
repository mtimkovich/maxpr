# MaxPR for [Smash.gg][1]

MaxPR is a program to generate Elo ratings for given [smash.gg][1] brackets.

It can output the results as either an HTML page or as a table.

The Elo is calculated using using the [TrueSkill][2] library.

## Dependencies

- [TrueSkill][2]
- [pysmash][4]
- [Mako][3]

## Setup

```
cd src
virtualenv --clear env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

`maxpr.py` takes one argument, which is a file with all tournaments to scrape from, with each tournament on a separate line.
Be sure to use the entire smash.gg bracket URL e.g. https://smash.gg/tournament/get-smashed-at-the-foundry-101/events/melee-singles/brackets/79121. Look at the `sample_input_file.txt` for an example of how it should look.
The tournaments *must* be in chronological order, otherwise the generated
ratings will be incorrect. Lines starting with a '#' will be ignored.

The `--html` flag can be given to generate the html page.

`--title` can be used to set the name of your tournament series on the generated html page.

The `--tag-map` can be given to a JSON file (see `remap.json` for an example) containing mappings from one tag to another. You can use this for players with multiple tags, particularly players without [smash.gg][1] accounts.

## Issues

Please let me know if you run into any issues by [filing a bug][issue].

[1]: http://smash.gg
[2]: http://trueskill.org
[3]: http://www.makotemplates.org
[4]: https://github.com/PeterCat12/pysmash
[issue]: https://github.com/mtimkovich/smash_maxpr/issues
