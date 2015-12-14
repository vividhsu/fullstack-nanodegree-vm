-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


drop database if exists tournament;

create database tournament;

\c tournament;

create table players (
    players_id serial primary key,
    name text
);

create table matches (
    matches_id serial primary key,
    winner serial references players(players_id),
    loser serial references players(players_id)
);