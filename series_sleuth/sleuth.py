import os
import json
import blaseball_core_game_data as gd
from .util import NoMatchingGames, SEASON_MAX, PLAYOFFS_MAX

class SleuthData(object):
    """
    Note: currently this class does things inefficiently,
    we go through the entire data set for each thing.
    A better way would be to use the parser class, pass
    one game data json item at a time, and accumulate
    each metric in a variable. Then the final json would
    throw all of them together. (But it is still super fast.)
    """
    def __init__(self, options):
        """Load the data set"""
        self.data = json.loads(gd.get_games_data())

        if options.game_id:
            self.game_record = None
            for j in self.data:
                if j['id']==options.game_id:
                    self.game_record = j
                    break
        else:
            self.game_record = None
            for j in self.data:
                # Careful with season and day, zero-indexed in self.data and one-indexed in options
                is_our_s = str(j['season']+1)==options.season
                is_our_d = str(j['season']+1)==options.season
                is_our_t = j['homeTeamNickname']==options.team or j['awayTeamnickname']==options.team
                if is_our_s and is_our_d and is_our_t:
                    self.game_record = j

        if self.game_record is None:
            raise NoMatchingGames()

        self.game_id = self.game_record['id']

        # Useful to know for playoffs calculations
        # Last day of playoffs, zero-indexed
        self.last_day0 = 0
        for j in self.data:
            if j['season']==self.game_record['season']:
                if j['day']>self.last_day0:
                    self.last_day0 = j['day']
        self.last_day = self.last_day0 + 1

    def get_id(self):
        return self.game_id

    def parse(self):
        """
        This takes the current game id and does a few on-the-fly calculations to return the following dict:
        (season/day are 1-indexed)

        {
            homeTeam: Millennials,
            awayTeam: Shoe Thieves,
            winner: home,
            season: 5,
            day: 104,
            playoffs: True,
            playoffsRound: 1,
            finalScore: {
                Millennials: 11,
                Shoe Thieves: 10
            },
            odds: {
                Millennials: 54,
                Shoe Thieves: 46
            },
            seasonRecord: {
                Millennials: [32, 17],
                Shoe Thieves: [30, 19]
            },
            seasonRecordFinal: {
                Millennials: [X, Y],
                Shoe Thieves: [Y, X]
            },
            opponentSeasonRecord: {
                Millennials: [5, 4],
                Shoe Thieves: [4, 5]
            },
            opponentSeasonRecordFinal: {
                Millennials: [X, Y],
                Shoe Thieves: [Y, X]
            },
            seasonRunsVersusOpponent: {
                Millennials: 35,
                Shoe Thieves: 35
            },
            seasonRunsVersusOpponentFinal: {
                Millennials: 35,
                Shoe Thieves: 35
            },
            playoffsRecord: {
            },
            playoffsRecordFinal: {
            },
            opponentPlayoffsRecord: {
            },
            opponentPlayoffsRecordFinal: {
            },
            playoffsRunsVersusOpponent: {
            },
            playoffsRunsVersusOpponentFinal: {
            },
            seriesRunsVersusOpponent: {
                Millennials: 5,
                Shoe Thieves: 6
            },
            seriesRunsVersusOpponentFinal: {
                Millennials: 32,
                Shoe Thieves: 28
            },
            seriesScore: {
                Millennials: 0,
                Shoe Thieves, 1
            },
            seriesScoreFinal: {
                Millennials: 1,
                Shoe Thieves: 2
            }
        }
        """
        # The final data structure returned
        sleuth_data = {}
        d = self.data
        r = self.game_record

        ht = r['homeTeamNickname']
        at = r['awayTeamNickname']
        season0 = r['season']
        season = season0 + 1
        day0 = r['day']
        day = day0 + 1

        sleuth_data['homeTeam'] = ht
        sleuth_data['awayTeam'] = at
        sleuth_data['winner'] = r['whoWon']
        sleuth_data['season'] = season
        sleuth_data['day'] = day
        sleuth_data['playoffs'] = False

        if day0 >= SEASON_MAX:
            sleuth_data['playoffs'] = True

        # 0 means not playoffs, will set this later for playoffs games
        sleuth_data['playoffsRound'] = 0

        # -------------------
        # Game things:

        # final_score
        sleuth_data['finalScore'] = {
            ht: r['homeScore'],
            at: r['awayScore']
        }

        # odds
        sleuth_data['odds'] = {
            ht: int(round(100*r['homeOdds'])),
            at: int(round(100*r['awayOdds']))
        }

        # -------------------
        # Season things:

        # season w/l record
        sleuth_data['seasonRecord'] = {
            ht: self.season_record(ht, season, day),
            at: self.season_record(at, season, day)
        }
        if sleuth_data['playoffs']:
            # playoffs w/l record
            sleuth_data['playoffsRecord'] = {
                ht: self.playoffs_record(ht, season, day),
                at: self.playoffs_record(at, season, day)
            }

        # final season w/l record
        sleuth_data['seasonRecordFinal'] = {
            ht: self.season_record(ht, season, SEASON_MAX),
            at: self.season_record(at, season, SEASON_MAX)
        }
        if sleuth_data['playoffs']:
            # final playoffs w/l record
            sleuth_data['playoffsRecordFinal'] = {
                ht: self.playoffs_record(ht, season, PLAYOFFS_MAX),
                at: self.playoffs_record(at, season, PLAYOFFS_MAX)
            }

        # season w/l record versus opponent
        opp = self.opponent_season_record(ht, at, season, day)
        sleuth_data['opponentSeasonRecord'] = {
            ht: opp,
            at: list(reversed(opp))
        }
        if sleuth_data['playoffs']:
            # playoffs w/l record versus opponent
            opp = self.opponent_playoffs_record(ht, at, season, day)
            sleuth_data['opponentPlayoffsRecord'] = {
                ht: opp,
                at: list(reversed(opp))
            }

        # final season w/l record versus opponent
        opp = self.opponent_season_record(ht, at, season, SEASON_MAX)
        sleuth_data['opponentSeasonRecordFinal'] = {
            ht: opp,
            at: list(reversed(opp))
        }
        if sleuth_data['playoffs']:
            # final playoffs w/l record versus opponent
            opp = self.opponent_playoffs_record(ht, at, season, PLAYOFFS_MAX)
            sleuth_data['opponentPlayoffsRecordFinal'] = {
                ht: opp,
                at: list(reversed(opp))
            }

        # season runs versus opponent
        oppr = self.opponent_season_runs(ht, at, season, day)
        sleuth_data['seasonRunsVersusOpponent'] = {
            ht: oppr[0],
            at: oppr[1]
        }
        if sleuth_data['playoffs']:
            # playoffs runs versus opponent
            oppr = self.opponent_playoffs_runs(ht, at, season, day)
            sleuth_data['playoffsRunsVersusOpponent'] = {
                ht: oppr[0],
                at: oppr[1]
            }

        # final season runs versus opponent
        oppr = self.opponent_season_runs(ht, at, season, SEASON_MAX)
        sleuth_data['seasonRunsVersusOpponentFinal'] = {
            ht: oppr[0],
            at: oppr[1]
        }
        if sleuth_data['playoffs']:
            # final playoffs runs versus opponent
            oppr = self.opponent_playoffs_runs(ht, at, season, PLAYOFFS_MAX)
            sleuth_data['playoffsRunsVersusOpponentFinal'] = {
                ht: oppr[0],
                at: oppr[1]
            }

        # -------------------
        # Series things:

        if day > SEASON_MAX:
            res = self.series_scores_playoffs(ht, at, season, day)
        else:
            res = self.series_scores(ht, season, day)

        # Series score and final series score
        ss = {ht: 0, at: 0}
        ssf = {ht: 0, at: 0}
        sruns = {ht: 0, at: 0}
        srunsf = {ht: 0, at: 0}
        for series_day, series_score in zip(res['days'], res['scores']):

            if series_day < day:
                # Series score, until current game
                if series_score[ht] > series_score[at]:
                    ss[ht] += 1
                elif series_score[at] > series_score[ht]:
                    ss[at] += 1

                # Series runs, until current game
                sruns[ht] += series_score[ht]
                sruns[at] += series_score[at]

            # Series score, final
            try:
                if series_score[ht] > series_score[at]:
                    ssf[ht] += 1
                elif series_score[at] > series_score[ht]:
                    ssf[at] += 1
            except:
                continue


            # Series runs, final
            srunsf[ht] += series_score[ht]
            srunsf[at] += series_score[at]

        sleuth_data['seriesScore'] = ss
        sleuth_data['seriesScoreFinal'] = ssf
        sleuth_data['seriesRunsVersusOpponent'] = sruns
        sleuth_data['seriesRunsVersusOpponentFinal'] = srunsf
        if sleuth_data['playoffs']:
            sleuth_data['playoffsRound'] = res['playoffsRound']

        return sleuth_data

    def season_record(self, team, season, day):
        """
        Returns the season W/L record for the given
        team UP TO BUT NOT INCLUDING the specified
        season and day (does not incl playoffs)

        Format is a list [X, Y]
        (X = n wins, Y = n losses)

        Season and day parameters are 1-indexed.
        To get a team's season record, pass in day 100.
        """
        wl = [0, 0]
        day0 = day - 1
        season0 = season - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']<SEASON_MAX:
                    if j['day']<day0:
                        if j['homeTeamNickname']==team:
                            if j['whoWon']=='home':
                                wl[0] += 1
                            else:
                                wl[1] += 1
                        elif j['awayTeamNickname']==team:
                            if j['whoWon']=='away':
                                wl[0] += 1
                            else:
                                wl[1] += 1
        return wl

    def playoffs_record(self, team, season, day):
        """
        Returns the playoffs W/L record for the given
        team UP TO BUT NOT INCLUDING the specified
        season and day.

        Format is a list [X, Y]
        (X = n wins, Y = n losses)

        Season and day parameters are 1-indexed.
        """
        wl = [0, 0]
        day0 = day - 1
        season0 = season - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']>=SEASON_MAX:
                    if j['day']<day0:
                        if j['homeTeamNickname']==team:
                            if j['whoWon']=='home':
                                wl[0] += 1
                            else:
                                wl[1] += 1
                        elif j['awayTeamNickname']==team:
                            if j['whoWon']=='away':
                                wl[0] += 1
                            else:
                                wl[1] += 1
        return wl

    def opponent_season_record(self, team, versus_team, season, day):
        """
        Returns season W/L record of the given team against
        the given opponent. (The opponent's record
        is just the reverse, of course.)
        Does not include playoffs.

        Format is a list [X, Y]
        (X = n wins, Y = n losses)

        Season and day parameters are 1-indexed.
        """
        wl = [0, 0]
        day0 = day - 1
        season0 = season - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']<SEASON_MAX:
                    if j['day']<day0:
                        if j['homeTeamNickname']==team and j['awayTeamNickname']==versus_team:
                            if j['whoWon']=='home':
                                wl[0] += 1
                            else:
                                wl[1] += 1
                        elif j['awayTeamNickname']==team and j['homeTeamNickname']==versus_team:
                            if j['whoWon']=='away':
                                wl[0] += 1
                            else:
                                wl[1] += 1
        return wl

    def opponent_playoffs_record(self, team, versus_team, season, day):
        """
        Returns playoffs W/L record of the given team against
        the given opponent. (The opponent's record
        is just the reverse, of course.)

        Format is a list [X, Y]
        (X = n wins, Y = n losses)

        Season and day parameters are 1-indexed.
        """
        wl = [0, 0]
        day0 = day - 1
        season0 = season - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']>=SEASON_MAX:
                    if j['day']<day0:
                        if j['homeTeamNickname']==team and j['awayTeamNickname']==versus_team:
                            if j['whoWon']=='home':
                                wl[0] += 1
                            else:
                                wl[1] += 1
                        elif j['awayTeamNickname']==team and j['homeTeamNickname']==versus_team:
                            if j['whoWon']=='away':
                                wl[0] += 1
                            else:
                                wl[1] += 1
        return wl

    def opponent_season_runs(self, team, versus_team, season, day):
        """
        Returns the total number of runs scored by each team
        when playing each other during regular season games,
        up to but not including the given day (does not include
        playoffs).

        Format is a list [X, Y]
        (X = n runs by team, Y = n runs by versus_team)

        Season and day parameters are 1-indexed.
        """
        runs = [0, 0]
        day0 = day - 1
        season0 = season - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']<SEASON_MAX:
                    if j['day']<day0:
                        if j['homeTeamNickname']==team and j['awayTeamNickname']==versus_team:
                            runs[0] += j['homeScore']
                            runs[1] += j['awayScore']
                        elif j['awayTeamNickname']==team and j['homeTeamNickname']==versus_team:
                            runs[0] += j['awayScore']
                            runs[1] += j['homeScore']
        return runs

    def opponent_playoffs_runs(self, team, versus_team, season, day):
        """
        Returns the total number of runs scored by each team
        when playing each other during regular season games,
        up to but not including the given day (does not include
        playoffs).

        Format is a list [X, Y]
        (X = n runs by team, Y = n runs by versus_team)

        Season and day parameters are 1-indexed.
        """
        runs = [0, 0]
        day0 = day - 1
        season0 = season - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']>=SEASON_MAX:
                    if j['day']<day0:
                        if j['homeTeamNickname']==team and j['awayTeamNickname']==versus_team:
                            runs[0] += j['homeScore']
                            runs[1] += j['awayScore']
                        elif j['awayTeamNickname']==team and j['homeTeamNickname']==versus_team:
                            runs[0] += j['awayScore']
                            runs[1] += j['homeScore']
        return runs

    def series_scores(self, team, season, day):
        """
        For a given team, season, and day,
        compile a list of all scores of all games
        in this 3-game series and return it,
        along with info about game dates.

        The user can use this to figure out:
        - which game in the series was a particular day
        - what was series score on that day
        - what was series score at end
        - how many runs did each team score in series

        {
            "season": 2,
            "days": [81, 82, 83],
            "scores": [
                {"AA": 9, "BB": 0},
                {"AA": 0, "BB": 8},
                {"AA": 3, "BB": 5}
            ]
        }

        The day and season parameters are one-indexed.
        """
        assert day <= SEASON_MAX
        day0 = day - 1
        ht = self.game_record['homeTeamNickname']
        at = self.game_record['awayTeamNickname']

        result = {
            "days": [],
            "scores": []
        }

        # Every regular-season series lasts 3 games.
        # Dividing the day mod 3 gives the series index.
        SL = 3
        series_start_day0 = (day0//SL)*SL
        series_end_day0 = series_start_day0 + SL - 1
        series_index = day0%SL

        season0 = season - 1
        seasons_games = [j for j in self.data if j['season']==season0]
        for this_day0 in range(series_start_day0, series_end_day0+1):
            this_day = this_day0 + 1
            todays_games = [j for j in seasons_games if j['day']==this_day0]
            our_game = [j for j in todays_games if (j['homeTeamNickname']==team or j['awayTeamNickname']==team)]
            assert len(our_game)>0
            our_game = our_game[0]
            score = {
                our_game['homeTeamNickname']: our_game['homeScore'],
                our_game['awayTeamNickname']: our_game['awayScore']
            }
            result['days'] = result['days'] + [this_day]
            result['scores'] = result['scores'] + [score]

        return result

    def series_scores_playoffs(self, team, versus_team, season, day):
        """
        For the given team, season, and day,
        compile a list of all scores of all games
        in this postseason 5-game series and return it,
        along with info about game dates.

        The user can use this to figure out:
        - which game in the series was a particular day
        - what was series score on that day
        - what was series score at end
        - how many runs did each team score in series

        {
            "playoffsRound": 1,
            "season": 2,
            "days": [100, 101, 102, 103, 104]
            "scores": [
                {"AA": 9, "BB": 0},
                {"AA": 0, "BB": 8},
                {"AA": 3, "BB": 5}
                {"AA": 3, "BB": 2}
                {"AA": 3, "BB": 1}
            ]
        }

        The day and season parameters are one-indexed.
        So are the days returned.
        """
        assert day > SEASON_MAX
        ht = self.game_record['homeTeamNickname']
        at = self.game_record['awayTeamNickname']

        result = {
            "days": [],
            "scores": []
        }

        # Every playoffs series lasts 5 games, but not all playoffs series
        # are 5 games, so day number does not give you series index.

        # Loop structure:
        # Start at day 100, loop over each day
        # Check if team name matches our team, and if opponent matches opponent on our day
        # If so, add day to days list, and add score to scores list
        playoffs_round = 0
        opponents = set()
        season0 = season - 1
        day0 = day - 1
        seasons_games = [j for j in self.data if j['season']==season0]
        for playoffs_day in range(100, self.last_day+1):
            # Find the JSON for all games on this day,
            # then find the one with the specified team
            playoffs_day0 = playoffs_day - 1
            todays_games = [j for j in seasons_games if j['day']==playoffs_day0]
            our_game = [j for j in todays_games if (j['homeTeamNickname']==team or j['awayTeamNickname']==team)]
            if len(our_game)==0:
                # Team did not play this day
                continue
            our_game = our_game[0]

            # Update opponents we have seen
            if our_game['homeTeamNickname']==team:
                opponents.add(our_game['awayTeamNickname'])
            elif our_game['awayTeamNickname']==team:
                opponents.add(our_game['homeTeamNickname'])

            # If we have reached the date of the game the user specified,
            # determine the playoffs round number
            if playoffs_day0 == day0:
                playoffs_round = len(opponents)

            # If versus team is correct too, record the score in a dict
            if (our_game['homeTeamNickname']==versus_team or our_game['awayTeamNickname']==versus_team):
                score = {
                    our_game['homeTeamNickname']: our_game['homeScore'],
                    our_game['awayTeamNickname']: our_game['awayScore']
                }

                # Append days and corresponding scores to final data structure
                result['days'] = result['days'] + [playoffs_day]
                result['scores'] = result['scores'] + [score]

        if playoffs_round == 0:
            raise Exception("Error playoffs_round is still 0 after going through all playoffs games")

        result['playoffsRound'] = playoffs_round
        result['season'] = season
        return result







    #################################################

    def home_wl_record(self, team, season, day):
        """
        Return the home W/L record for the given
        team UP TO BUT NOT INCLUDING the specified
        season and day. (Includes postseason games.)

        Format is a list [X, Y]
        (X = n wins, Y = n losses)

        Season and day parameters are 1-indexed.
        """
        wl = [0, 0]
        season0 = season - 1
        day0 = day - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']<day0:
                    if j['homeTeamNickname']==team:
                        if j['whoWon']=='home':
                            wl[0] += 1
                        else:
                            wl[1] += 1
        return wl

    def away_wl_record(self, team, season, day):
        """
        Return the away W/L record for the given
        team UP TO BUT NOT INCLUDING the specified
        season and day. (Includes postseason games.)

        Format is a list [X, Y]
        (X = n wins, Y = n losses)
        """
        wl = [0, 0]
        season0 = season - 1
        day0 = day - 1
        for j in self.data:
            if j['season']==season0:
                if j['day']<day0:
                    if j['awayTeamNickname']==team:
                        if j['whoWon']=='away':
                            wl[0] += 1
                        else:
                            wl[1] += 1
        return wl

