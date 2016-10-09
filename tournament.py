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
    db = connect()
    c = db.cursor()
    c.execute("UPDATE game SET wins = 0, losses = 0")
    c.execute("DELETE from matches")
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE from game")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT COALESCE(count(player_id),0) FROM game")
    rows = c.fetchall()
    db.commit()
    db.close()
    #print str(rows) + " THIS IS ROWS"
    for row in rows:
        result = row[0]
        #print str(result) + " THIS IS RESULT"
    return result



def registerPlayer(name):
    """Adds a player to the tournament database.
    
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = str(name)
    db = connect()
    c = db.cursor()
    c.execute("INSERT INTO game (player_name) VALUES (%s)", (name,))
    print name + " REGISTERED"
    db.commit()
    db.close()

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
    db = connect()
    c = db.cursor()
    c.execute("""  SELECT game.player_id, player_name, wins, matches
                   FROM 
                   (SELECT player_id, COALESCE(wins, 0) + COALESCE(losses, 0) as matches
                   FROM game GROUP BY player_id, wins, losses) as subq
                   JOIN game ON (game.player_id = subq.player_id)
                   ORDER BY wins
                   
                   
                   
              """)
    rows = c.fetchall()
    print rows,
    print ": THIS IS STANDINGS NOW"
    return rows
    db.commit()
    db.close()

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    #winner = int(winner)
    #loser = int(loser)
    if (winner < 1 or loser < 1):
        raise ValueError("player id's must both be greater than zero")
    db = connect()
    c = db.cursor()
    #c.execute("SELECT * FROM matches")
    c.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s, %s)", (winner, loser,))
    c.execute("UPDATE game SET wins = wins + 1 WHERE player_id = %s", (winner,))
    c.execute("UPDATE game SET losses = losses + 1 WHERE player_id = %s", (loser,))
    print winner, loser, 
    print " These are winner, loser"
    #rows = c.fetchall()
    #return rows
    db.commit()
    db.close()

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
    result = []
    players = playerStandings()

    for i in range(0, len(players), 2):
        result.append(
                (players[i][0], players[i][1], players[i+1][0], players[i+1][1])
            )
    return result

def select_all(table):
    db = connect()
    c = db.cursor()
    c.execute("SELECT * FROM %s", (table,))
    db.commit()
    db.close()

