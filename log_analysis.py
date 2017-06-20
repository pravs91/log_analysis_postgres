#!/bin/env python2.7

import psycopg2
import sys


def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a database connection.
    Raise error if exception occurs."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        return db
    except psycopg2.Error as e:
        print "Unable to connect to database %s" % database_name
        sys.exit(1)


# common function to execute a query
def executeQuery(query):
    conn = connect("news")
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows


def getMostArticleViews():
    query = "SELECT title, views FROM articleViews LIMIT 3;"
    rows = executeQuery(query)
    print "1. The three most popular articles of all time are:\n"
    for row in rows:
        print "\t%s - %s views" % (row[0], row[1])


def getMostAuthorViews():
    query = "SELECT name, sum(views) as count FROM articleViews JOIN authors\
        on authors.id = articleViews.author group by name\
        order by count desc LIMIT 3;"
    rows = executeQuery(query)
    print "2. The three most popular authors of all time by article views:\n"
    for row in rows:
        print "\t%s - %s views" % (row[0], row[1])


def getErrorDates():
    query = "SELECT requests.time,\
        (errors.errors::float / requests.requests) * 100.0\
        as ratio from requests, errors where requests.time = errors.time\
        order by ratio desc;"
    rows = executeQuery(query)
    print "3. The days when more than 1% of requests led to errors:\n"
    for row in rows:
        if(row[1] > 1.0):
            print "\t%s - %s %% errors" %\
                (row[0].strftime("%d %B, %Y"), round(row[1], 2))
        else:
            break  # because the results are sorted in desc order

if __name__ == '__main__':
    getMostArticleViews()
    getMostAuthorViews()
    getErrorDates()
