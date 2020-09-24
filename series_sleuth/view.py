import sys
import json
from .util import get_short2long
from .sleuth import SleuthData

class BaseView(object):
    """
    View class for series sleuth.
    - create an object to wrap the game info
    - create an object (or method) to parse the data, create the series summary
    - display the game summary using format-specific methods
    """
    def __init__(self, options):
        """
        Create the data wrapper class here
        """
        self.data = SleuthData(options)
        self.game_id = self.data.get_id()

class JsonView(BaseView):
    def show(self):
        print(json.dumps(self.data.parse(), indent=4))

class TextView(BaseView):
    def show(self):
        """
        Charleston Shoe Thieves @ New York Millennials
        Season 5, Day 104
        Game N, Best of N
        Playoffs Round N
        
        Final Score:
        Millenials      11
        Shoe Thieves    10

        Odds:
        Millennials:    54%
        Shoe Thieves:   46%

        Overall Record:
        Millennials     32-17
        Shoe Thieves    30-19

        Record vs Opponent:
        Millennials     5-4
        Shoe Thieves    4-5

        Runs vs Opponent:
        Millennials     35
        Shoe Thieves    35

        Series Runs vs Opponent (up to current game):
        Millennials     5
        Shoe Thieves    6

        Series Runs vs Opponent (final):
        Millennials     32
        Shoe Thieves    28

        Series Score (up to current game):
        Millennials     0
        Shoe Thieves    1

        Series Score (final):
        Millennials     2
        Shoe Thieves    3
        """
        data = self.data.parse()
        ht = data['homeTeam']
        at = data['awayTeam']
        short2long = get_short2long()
        htlong = short2long[ht]
        atlong = short2long[at]

        # Header
        header = []
        header.append("%s @ %s"%(atlong, htlong))
        header.append("Season %d, Day %d"%(data['season'], data['day']))
        which_game = data['seriesScore'][ht] + data['seriesScore'][at] + 1
        if data['playoffs']:
            bestof = 5
        else:
            bestof = 3
        header.append("Game %d, Best of %d"%(which_game, bestof))
        if data['playoffs']:
            header.append("Playoffs Round %d"%(data['playoffsRound']))

        # Body
        labels_map = {
            'finalScore': 'Final Score',
            'odds': 'Odds',
            'overallRecord': 'Overall WL Record (season, up to current game)',
            'opponentRecord': 'WL Record vs Opponent (season, up to current game)',
            'runsVersusOpponent': 'Runs vs Opponent (season, up to current game)',
            'seriesRunsVersusOpponent': 'Runs vs Opponent (series, up to current game)',
            'seriesRunsVersusOpponentFinal': 'Runs vs Opponent (series, final)',
            'seriesScore': 'Series Record (up to current game)',
            'seriesScoreFinal': 'Series Record (final)',
        }
        body = []
        for label, description in labels_map.items():
            body.append(description + ":")
            if label in ['opponentRecord', 'overallRecord']:
                body.append("%-30s%s"%(at, "-".join([str(j) for j in data[label][at]])))
                body.append("%-30s%s"%(ht, "-".join([str(j) for j in data[label][ht]])))
            elif label in ['odds']:
                body.append("%-30s%s%%"%(at, data[label][at]))
                body.append("%-30s%s%%"%(ht, data[label][ht]))
            else:
                body.append("%-30s%s"%(at, data[label][at]))
                body.append("%-30s%s"%(ht, data[label][ht]))
            body.append("")

        text = header + [""] + body
        print("\n".join(text))
