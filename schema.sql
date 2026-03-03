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
  color TEXT,
  breed TEXT REFERENCES Dog_breeds(name),
  birth_date DATE,
  death_date DATE,
  sex TEXT CHECK (sex IN ('M', 'F')),
  father_id TEXT REFERENCES Dogs(id),
  mother_id TEXT REFERENCES Dogs(id),
  owner_id INTEGER REFERENCES Users(id),
  picture INTEGER REFERENCES Pictures(id),
  litters INTEGER REFERENCES Litters(id),
  championship_title INTEGER REFERENCES Championship_titles(id),
  best_test INTEGER CHECK (best_test IN (1, 2, 3, 4, 5)),
  best_show INTEGER REFERENCES Dog_shows(id),
  litter_score TEXT,
  score_trace TEXT,
  hip_index INTEGER,
  use_index INTEGER
);

CREATE TABLE Championship_titles (
  id INTEGER PRIMARY KEY,
  title, TEXT UNIQUE
);

CREATE TABLE Dog_breeds (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE Pictures (
  id INTEGER PRIMARY KEY,
  dog_id INTEGER REFERENCES Dogs(id),
  url TEXT
);

CREATE TABLE Dog_shows (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  date DATE
);

CREATE TABLE Litters (
  id INTEGER PRIMARY KEY,
  father_id TEXT REFERENCES Dogs(id),
  mother_id TEXT REFERENCES Dogs(id),
  birth_date DATE
);
