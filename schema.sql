CREATE TABLE Users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE,
  email TEXT UNIQUE,
  password_hash TEXT
);

CREATE TABLE Dogs (
  id INTEGER PRIMARY KEY,
  registration_number TEXT UNIQUE,
  name TEXT,
  breed TEXT REFERENCES DogBreeds(name),
  born_date DATE,
  sex TEXT CHECK (sex IN ('M', 'F')),
  father_id TEXT REFERENCES Dogs(registration_number),
  mother_id TEXT REFERENCES Dogs(registration_number),
  owner_id INTEGER REFERENCES Users(id),
  picture INTEGER REFERENCES Pictures(id),
  litters INTEGER REFERENCES Litters(id),
  championship_title TEXT CHECK (championship_title IN ('KVA', 'KV', 'KVA2', 'KV2', 'KVA3', 'KV3', 'KVA4', 'KV4', 'KVA5', 'KV5', 'KVA6', 'KV6', 'KVA7', 'KV7', 'KVA8', 'KV8', 'KVA9', 'KV9')),
  best_test INTEGER CHECK (best_test IN (1, 2, 3, 4, 5)),
  best_show TEXT,
  litter_score TEXT,
  score_trace TEXT,
  hip_index INTEGER,
  use_index INTEGER
);

CREATE TABLE DogBreeds (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE Pictures (
  id INTEGER PRIMARY KEY,
  dog_id INTEGER REFERENCES Dogs(id),
  url TEXT
);

CREATE TABLE DogShows (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  date DATE
);

CREATE TABLE Litters (
  id INTEGER PRIMARY KEY,
  father_id TEXT REFERENCES Dogs(registration_number),
  mother_id TEXT REFERENCES Dogs(registration_number),
  born_date DATE
);
