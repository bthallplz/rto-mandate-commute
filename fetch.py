#!/usr/bin/python3

# SPDX-License-Identifier: MIT

from datetime import datetime

import sqlite3
import sys
import time

# TODO: Repurpose this for getting and sticking in the API key for the Google Maps API
if len(sys.argv) > 1:
    force = True

# TODO: Read in the Google Maps API key via an argument, so we don't leak the API key

database = sqlite3.connect("commute_data.db")
database.row_factory = sqlite3.Row

c = database.cursor()

c.execute("SELECT * FROM commutes")

for commute in c.fetchall():
    print(commute["name"])

    try:
        # TODO: Insert the data fields from the Google Maps API response into the db
        """
        TODO: Use this for current time:
            `datetime.strftime(datetime.now(),
                "%d %B %Y %H:%M")`
        """
        try:
            c.execute(
                # TODO: Add in other data fields we're gathering from API response + time of initiating all commutes (this time around)
                """INSERT INTO trips (commute_id, duration_in_traffic_seconds) VALUES (?, ?)""",
                (commute["id"],2) # Seems to require a tuple, so needs a trailing comma if only one element
            )
        except ValueError:
            pass

    except RuntimeError:
        print("failed")
        pass

    print(" ")

database.commit()
database.close()
