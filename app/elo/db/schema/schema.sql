CREATE TABLE players (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE n64 (
  id INTEGER PRIMARY KEY,
  mu REAL NOT NULL,
  sigma REAL NOT NULL,
  last_mu, REAL,
  id_player INTEGER NOT NULL,
  FOREIGN KEY(id_player) REFERENCES players(id)
);

CREATE TABLE melee (
  id INTEGER PRIMARY KEY,
  mu REAL NOT NULL,
  sigma REAL NOT NULL,
  last_mu, REAL,
  id_player INTEGER NOT NULL,
  FOREIGN KEY(id_player) REFERENCES players(id)
);

CREATE TABLE brawl (
  id INTEGER PRIMARY KEY,
  mu REAL NOT NULL,
  sigma REAL NOT NULL,
  last_mu, REAL,
  id_player INTEGER NOT NULL,
  FOREIGN KEY(id_player) REFERENCES players(id)
);

CREATE TABLE smash4 (
  id INTEGER PRIMARY KEY,
  mu REAL NOT NULL,
  sigma REAL NOT NULL,
  last_mu, REAL,
  id_player INTEGER NOT NULL,
  FOREIGN KEY(id_player) REFERENCES players(id)
);

CREATE TABLE matches (
  id INTEGER PRIMARY KEY,
  winners TEXT NOT NULL,
  losers TEXT NOT NULL,
  game TEXT NOT NULL
);
