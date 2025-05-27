#!/usr/bin/python3

# SPDX-License-Identifier: MIT

import configparser
import sqlite3
import sys


# TODO: Check if database file exists
database = sqlite3.connect("commute_data.db")
database.execute("PRAGMA foreign_keys = 1") # enabling foreign keys

c = database.cursor()

try:
    c.execute(
        """CREATE TABLE commutes
                (id integer primary key autoincrement,
                name text UNIQUE,
                home_location text,
                work_location text)
            """
    )
    
    c.execute(
        """CREATE TABLE trips
                (id integer primary key autoincrement,
                commute_id integer,
                trip_datetime datetime,
                duration_in_traffic_seconds integer,
                destination text,
                FOREIGN KEY(commute_id) REFERENCES commutes(id))
            """
    )
except:
    print("Database tables already created.")

# TODO: Read in the configs for commutes
if len(sys.argv) > 1:
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    # TODO: Plan how the commutes .ini files should work/be structured
    for section in config.sections():
        if section == "Planet":
            continue
        print(f"{section}: from '{config[section]['home_location']}' to '{config[section]['work_location']}' and vice versa")
        c.execute(
            f"""INSERT INTO commutes (name, home_location, work_location) VALUES
                  ("{section}", "{config[section]['home_location']}", "{config[section]['work_location']}")
                  ON CONFLICT(name) DO UPDATE SET
                    home_location=excluded.home_location,
                    work_location=excluded.work_location
                  """
        )

database.commit()
