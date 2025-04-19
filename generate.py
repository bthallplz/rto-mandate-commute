#!/usr/bin/python3

# SPDX-License-Identifier: MIT

from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import sqlite3
import time
import pathlib

SITE_NAME = "Developers Planet"
SITE_URL = "https://devplanet.one.pl/" # Provide a trailing backslash: /

MAX_ENTRIES_PER_FEED = 8


def filter_date(value, format='%d %B %Y'):
    return time.strftime(format, time.strptime(value, '%Y-%m-%d %H:%M:%S'))


conn = sqlite3.connect('feeds.db')
conn.row_factory = sqlite3.Row

c = conn.cursor()

c.execute('''SELECT name, url, etag, modified, id, blog_url
             FROM feeds
             ORDER BY name''')

feeds = c.fetchall()

c.execute('''SELECT f.name, f.blog_url, f.title as blog_title,
                    p.feed_id, p.title, p.url, p.post, p.published_date,
                    p.author
             FROM posts p, feeds f
             WHERE f.id = p.feed_id
				AND p.published_date > date('now', '-7 days')
             ORDER by p.published_date DESC''')

posts = c.fetchall()

conn.close()


pathlib.Path('output').mkdir(parents=True, exist_ok=True)


file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)
env.filters['date'] = filter_date

template = env.get_template('index.html.j2')

output = template.render(generate_time=datetime.strftime(datetime.now(),
                                                         "%d %B %Y %H:%M"),
                         posts=posts, feeds=feeds, site_name=SITE_NAME)

with open('output/index.html', 'w') as html:
    html.write(output)


template = env.get_template('titles_only.html.j2')

output = template.render(generate_time=datetime.strftime(datetime.now(),
                                                         "%d %B %Y %H:%M"),
                         posts=posts, feeds=feeds, site_name=SITE_NAME)

with open('output/titles_only.html', 'w') as html:
    html.write(output)


template = env.get_template('rss20.xml.j2')

output = template.render(generate_time=datetime.strftime(datetime.now(),
                                                         "%d %B %Y %H:%M"),
                         posts=posts, feeds=feeds, site_name=SITE_NAME, site_url=SITE_URL)

with open('output/rss20.xml', 'w') as rss:
    rss.write(output)
