import sys
import os
import json
import configargparse
from .view import TextView, JsonView
from .util import (
    get_league_division_team_data,
    CaptureStdout
)


def main(sysargs = sys.argv[1:]):

    p = configargparse.ArgParser()

    # These are safe for command line usage (no accent in Dale)
    _, _, ALLTEAMS = get_league_division_team_data()

    p.add('-v',
          '--version',
          required=False,
          default=False,
          action='store_true',
          help='Print program name and version number and exit')

    p.add('-c',
          '--config',
          required=False,
          is_config_file=True,
          help='config file path')

    # Option 1: specify game by ID
    p.add('-g',
          '--game-id',
          required=False,
          help='Specify the game ID of the game to summarize (repeat flag to specify multiple game IDs)')

    # Option 2: specify game by day, season, and team
    p.add('--team',
          required=False,
          choices=ALLTEAMS,
          action='append',
          help='Specify our team')
    p.add('--season',
          required=False,
          help='Specify season (this flag cannot be repeated for multiple seasons)')
    p.add('--day',
          required=False,
          help='Specify day (this flag cannot be repeated for multiple days)')

    # format
    g = p.add_mutually_exclusive_group()
    g.add('--text',
          action='store_true',
          default=False,
          help='Print game IDs in plain text format, one ID per line')
    g.add('--json',
          action='store_true',
          default=False,
          help='Print game IDs in JSON format, with additional data about the game')

    # -----

    # Print help, if no arguments provided
    if len(sysargs)==0:
        p.print_help()
        exit(0)

    # Parse arguments
    options = p.parse_args(sysargs)

    # If the user asked for the version,
    # print the version number and exit.
    if options.version:
        from . import _program, __version__
        print(_program, __version__)
        sys.exit(0)

    # If the user did not specify output format, use text
    if (not options.json) and (not options.text):
        options.json = True

    # User must specify team AND season AND day, OR game id
    tsd = options.team and options.season and options.day
    gid = options.game_id
    if not tsd and not gid:
        raise Exception("Error: you must specify either --game-id or all three of --team/--season/--day")

    if options.text:
        v = TextView(options)
        v.show()
    elif options.json:
        v = JsonView(options)
        v.show()


def series_sleuth(sysargs):
    with CaptureStdout() as so:
        main(sysargs)
    return str(so)


if __name__ == '__main__':
    main()
