-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE game (player_id SERIAL,
                   player_name TEXT,
                   wins INTEGER DEFAULT 0,
                   losses INTEGER DEFAULT 0)

CREATE TABLE matches (match_id SERIAL,
                      winner_id SERIAL,
                      loser_id SERIAL)