# blaseball-series-sleuth

This is a command line tool for getting information about blaseball game series.

## Table of Contents

* [What Information?](#what-information)
* [Example](#example)
* [Python API](#python-api)

## What Information?

The `series-sleuth` utility takes the following inputs:

* Game ID

and it returns the following outputs:

* Final score
* Odds for each team

* Season win/loss record before the game
* Season win/loss record final
* Versus opponent season win/loss record before the game
* Versus opponent season win/loss record final
* Season runs versus opponent before the game
* Season runs versus opponent final

* Playoffs win/loss record before the game
* Playoffs win/loss record final
* Versus opponent playoffs win/loss record before the game
* Versus opponent playoffs win/loss record final
* Playoffs runs versus opponent before the game
* Playoffs runs versus opponent final

* Series win/loss record before the game
* Series win/loss record final

* Series runs versus opponent before the game
* Series runs versus opponent final

## Example

Here is a quick example. First, we find a game ID using the
[`game-finder`](https://github.com/ch4zm/blaseball-game-finder)
command line tool, then we pass it to series-sleuth using the `-g`
(game ID) flag:

```text
$ game-finder --season 3 --day 103 --team Lovers
7e23e6d3-911e-45a6-87d2-3a2efbcbae6f
```

Now we can run the command like `series-sleuth --text -g <game-id>`, or we can
use xargs and pipes to pass the output of `game-finder` to the `series-sleuth`
command. We also include the `--text` flag to format the output as text:

```text
$ game-finder --season 3 --day 103 --team Lovers | xargs series-sleuth --text -g

San Francisco Lovers @ Charleston Shoe Thieves
Season 3, Day 103
Game 4, Best of 5
Playoffs Round 1

Final Score:
Lovers                    20
Shoe Thieves               6

Odds:
Lovers                    67%
Shoe Thieves              33%

Season WL Record (up to current game):
Lovers                 59-40
Shoe Thieves           59-40

Season WL Record (final):
Lovers                 58-40
Shoe Thieves           58-40

Season WL Record vs Opponent (up to current game):
Lovers                   1-2
Shoe Thieves             2-1

Season WL Record vs Opponent (final):
Lovers                   1-2
Shoe Thieves             2-1

Season Runs Scored vs Opponent (up to current game):
Lovers                    14
Shoe Thieves              14

Season Runs Scored vs Opponent (final):
Lovers                    14
Shoe Thieves              14

Playoffs WL Record (up to current game):
Lovers                   2-1
Shoe Thieves             1-2

Playoffs WL Record (final):
Lovers                   4-4
Shoe Thieves             1-3

Playoffs WL Record vs Opponent (up to current game):
Lovers                   2-1
Shoe Thieves             1-2

Playoffs WL Record vs Opponent (final):
Lovers                   3-1
Shoe Thieves             1-3

Playoffs Runs Scored vs Opponent (up to current game):
Lovers                    23
Shoe Thieves              10

Playoffs Runs Scored vs Opponent (final):
Lovers                    43
Shoe Thieves              16

Series Runs Scored vs Opponent (up to current game):
Lovers                    23
Shoe Thieves              10

Series Runs Scored vs Opponent (final):
Lovers                    43
Shoe Thieves              16

Series WL Record (up to current game):
Lovers                     2
Shoe Thieves               1

Series WL Record (final):
Lovers                     3
Shoe Thieves               1
```

If you prefer the data in JSON format, for parsing with other
utilities, you can pass the `--json` flag:

```text
$ game-finder --season 3 --day 103 --team Lovers | xargs series-sleuth --json -g
{
    "homeTeam": "Shoe Thieves",
    "awayTeam": "Lovers",
    "winner": "away",
    "season": 3,
    "day": 103,
    "playoffs": true,
    "playoffsRound": 1,
    "finalScore": {
        "Shoe Thieves": 6,
        "Lovers": 20
    },
    "odds": {
        "Shoe Thieves": 33,
        "Lovers": 67
    },
    "seasonRecord": {
        "Shoe Thieves": [
            59,
            40
        ],
        "Lovers": [
            59,
            40
        ]
    },
    "playoffsRecord": {
        "Shoe Thieves": [
            1,
            2
        ],
        "Lovers": [
            2,
            1
        ]
    },
    "seasonRecordFinal": {
        "Shoe Thieves": [
            58,
            40
        ],
        "Lovers": [
            58,
            40
        ]
    },
    "playoffsRecordFinal": {
        "Shoe Thieves": [
            1,
            3
        ],
        "Lovers": [
            4,
            4
        ]
    },
    "opponentSeasonRecord": {
        "Shoe Thieves": [
            2,
            1
        ],
        "Lovers": [
            1,
            2
        ]
    },
    "opponentPlayoffsRecord": {
        "Shoe Thieves": [
            1,
            2
        ],
        "Lovers": [
            2,
            1
        ]
    },
    "opponentSeasonRecordFinal": {
        "Shoe Thieves": [
            2,
            1
        ],
        "Lovers": [
            1,
            2
        ]
    },
    "opponentPlayoffsRecordFinal": {
        "Shoe Thieves": [
            1,
            3
        ],
        "Lovers": [
            3,
            1
        ]
    },
    "seasonRunsVersusOpponent": {
        "Shoe Thieves": 14,
        "Lovers": 14
    },
    "playoffsRunsVersusOpponent": {
        "Shoe Thieves": 10,
        "Lovers": 23
    },
    "seasonRunsVersusOpponentFinal": {
        "Shoe Thieves": 14,
        "Lovers": 14
    },
    "playoffsRunsVersusOpponentFinal": {
        "Shoe Thieves": 16,
        "Lovers": 43
    },
    "seriesScore": {
        "Shoe Thieves": 1,
        "Lovers": 2
    },
    "seriesScoreFinal": {
        "Shoe Thieves": 1,
        "Lovers": 3
    },
    "seriesRunsVersusOpponent": {
        "Shoe Thieves": 10,
        "Lovers": 23
    },
    "seriesRunsVersusOpponentFinal": {
        "Shoe Thieves": 16,
        "Lovers": 43
    }
}
```

## Python API

If you want to use the `series-sleuth` tool from Python instead of
using the command line tool, we provide a function that you can
import that will return the output of the command in a string.

Suppose we want to get the output of the following command
as a Python string:

```
$ series-sleuth --json -g e23e6d3-911e-45a6-87d2-3a2efbcbae6f
```

Then we can import the `series_sleuth()` function from the
`series_sleuth` module, and pass it the command line arguments
as a list of strings:

```
from series_sleuth.command import series_sleuth

flags = "--json -g e23e6d3-911e-45a6-87d2-3a2efbcbae6f"
flags = flags.split(" ")

result = series_sleuth(flags)
print(result)
```

