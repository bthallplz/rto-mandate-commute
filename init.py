#!/usr/bin/python3

# SPDX-License-Identifier: MIT

import configparser
import sqlite3
import sys

database = sqlite3.connect("commute_data.db")

c = database.cursor()

c.execute(
    """CREATE TABLE commutes
             (id integer primary key autoincrement,
              name text,
              title text,
              blog_url text,
              url text,
              etag text,
              modified text)
          """
)

c.execute(
    """CREATE TABLE trips
             (id integer primary key autoincrement,
             commute_id integer,
             author text,
             title text,
             post text,
             url text,
             published_date datetime)
          """
)

# TODO: Read in the configs for commutes
if len(sys.argv) > 1:
    """
    TODO: See if there's multiple system arguments.
        Check if the arguments matche some filename patterns,
            depending on which filename it matches, if any, do a certain thing
                (like setting some commutes' info to `private` visibility)
    """

    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    # TODO: Plan how the commutes .ini files should work/be structured
    for section in config.sections():
        if section == "Planet":
            continue
        print(f"{section} {config[section]['name']}")
        c.execute(
            f"""INSERT INTO commutes (name, url) VALUES
                  ("{config[section]['name']}", "{section}")"""
        )

database.commit()
