#!/usr/bin/python3

# SPDX-License-Identifier: MIT

from datetime import datetime

import sqlite3
import sys
import time
import googlemaps


if len(sys.argv) > 2:
    
    gmaps = googlemaps.Client(key=sys.argv[1]) # Setting the Google Maps API key via an argument we pass to the script

    if sys.argv[2] == "to-work":
        print('Going to work!\n')
        
        destination = "work"
    
    elif sys.argv[2] == "to-home":
        print('Going home! Finally!\n')
        
        destination = "home"
    
    else:
        print(
"""You need to set a second argument for the fetch.py script that specifies what the destination will be.
Say "to-work" if we're headed to work, or "to-home" if we're headed home."""
)
        destination = "unspecified"

    database = sqlite3.connect("commute_data.db")
    database.row_factory = sqlite3.Row

    c = database.cursor()

    c.execute("SELECT * FROM commutes")
    
    now = datetime.now()

    # Adapt the dates so we can continue to read them into SQLite
    def adapt_datetime_iso(val):
        """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
        return val.isoformat()

    sqlite3.register_adapter(datetime, adapt_datetime_iso)

    # Request the commute time in seconds from the Google Maps API
    def get_travel_time(from_loc, to_loc):
            directions_result = gmaps.directions(from_loc,
                                                to_loc,
                                                mode="driving",
                                                departure_time=now)

            return directions_result[0]['legs'][0]['duration_in_traffic']['value'] # In seconds
    
    
    for commute in c.fetchall():
        print(commute["name"], destination)
        
        home_to_work = 61 # Dummy amount of seconds for us to use while testing this, instead of making a request to the API - use get_travel_time() when live
        
        work_to_home = 161 # Dummy amount of seconds for us to use while testing this, instead of making a request to the API - use get_travel_time() when live

        print(
f'''Current time to work from home: {home_to_work / 60} minutes

Current time to home from work: {work_to_home / 60} minutes''')

        try:
            # TODO: Insert the data fields from the Google Maps API response into the db
            try:
                c.execute(
                    # TODO: Add in other data fields we're gathering from API response + time of initiating all commutes (this time around)
                    """INSERT INTO trips (commute_id, duration_in_traffic_seconds, trip_datetime) VALUES (?, ?, ?)""",
                    (commute["id"],home_to_work, now) # Seems to require a tuple, so needs a trailing comma if only one element
                )
            except ValueError:
                pass

        except RuntimeError:
            print("failed")
            pass

        print(" ")

    database.commit()
    database.close()

else:
    print(
"""Please provide two arguments along with this `fetch.py` script:

1. the Google Maps API key we should use when gathering commute times

2. the phrase that specifies what the destination will be. Say "to-work" if we're headed to work, or 'to-home' if we're headed home.""")
