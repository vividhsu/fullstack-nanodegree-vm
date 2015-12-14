#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from matches")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from players")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("select count(*) as num from players")
    count = cursor.fetchone()
    conn.close()
    return count[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into players (name) values (%s)", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings = []
    conn = connect()
    cursor = conn.cursor()
    query = """
            select wintable.id, wintable.name, wintable.win, losetable.lose from 
              (select players.players_id as id, players.name as name, 
                 count(matches.winner) as win 
              from players left join matches 
              on players.players_id = matches.winner 
              group by players.players_id order by win desc) as wintable 
            full join 
              (select players.players_id as id, count(matches.loser) as lose 
              from players left join matches 
              on players.players_id = matches.loser 
              group by players.players_id) as losetable 
            on wintable.id = losetable.id order by wintable.win
            """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    for res in result:
        total = int(res[2]) + int(res[3])
        new_res = (res[0], res[1], int(res[2]), total)
        standings.append(new_res)
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into matches (winner, loser) values (%s, %s)", (winner, loser,))
    conn.commit()
    conn.close()

def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    pairings = []
    standings = playerStandings()
    player_num = countPlayers()
    for i in range(0, player_num, 2):
        id1 = standings[i][0]
        name1 = standings[i][1]
        id2 = standings[i + 1][0]
        name2 = standings[i + 1][1]
        standing = (id1, name1, id2, name2)
        pairings.append(standing)
    return pairings



