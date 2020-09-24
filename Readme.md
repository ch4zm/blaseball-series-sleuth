# blaseball-series-sleuth

This is a command line tool for getting information about blaseball game series.

## What Information?

The `series-sleuth` utility takes the following inputs:

* Game ID

and it returns the following outputs:

* Final score
* Odds for each team
* Overall season win loss record for each team
* Season win loss record against this game's opponent
* Runs scored versus this game's opponent (season)
* Runs scored versus this game's opponent (series)
* Series win/loss record (up to current game)
* Series win/loss record (final)

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
Lovers                        20
Shoe Thieves                  6

Odds:
Lovers                        67%
Shoe Thieves                  33%

Overall WL Record (season, up to current game):
Lovers                        62-41
Shoe Thieves                  60-43

WL Record vs Opponent (season, up to current game):
Lovers                        4-3
Shoe Thieves                  3-4

Runs vs Opponent (season, up to current game):
Lovers                        57
Shoe Thieves                  30

Runs vs Opponent (series, up to current game):
Lovers                        23
Shoe Thieves                  10

Runs vs Opponent (series, final):
Lovers                        43
Shoe Thieves                  16

Series Record (up to current game):
Lovers                        2
Shoe Thieves                  1

Series Record (final):
Lovers                        3
Shoe Thieves                  1
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
    "overallRecord": {
        "Shoe Thieves": [
            60,
            43
        ],
        "Lovers": [
            62,
            41
        ]
    },
    "opponentRecord": {
        "Shoe Thieves": [
            3,
            4
        ],
        "Lovers": [
            4,
            3
        ]
    },
    "runsVersusOpponent": {
        "Shoe Thieves": 30,
        "Lovers": 57
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

