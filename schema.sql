CREATE TABLE Owners (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  email TEXT UNIQUE,
  password_hash TEXT
);

CREATE TABLE Dogs (
  id INTEGER PRIMARY KEY,
  registration_number TEXT UNIQUE,
  name TEXT,
  image BLOB,
  color TEXT REFERENCES Colors(name),
  breed TEXT REFERENCES Dog_breeds(name),
  date_of_birth DATE,
  date_of_death DATE,
  sex TEXT CHECK (sex IN ('Male', 'Female')),
  father_id TEXT REFERENCES Dogs(id),
  mother_id TEXT REFERENCES Dogs(id),
  owner_id INTEGER REFERENCES Owners(id),
  litter_id INTEGER REFERENCES Litters(id),
  best_test INTEGER CHECK (best_test IN (1, 2, 3, 4, 5)),
  best_show_id INTEGER REFERENCES Dog_shows(id),
  hip_index INTEGER,
  use_index INTEGER
);

CREATE TABLE Colors (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE Championship_titles (
  id INTEGER PRIMARY KEY,
  title TEXT UNIQUE
);

CREATE TABLE Dog_breeds (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE
);

CREATE TABLE Dog_shows (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  winner_id INTEGER REFERENCES Dogs(id),
  date DATE
);

CREATE TABLE Show_participants (
  id INTEGER PRIMARY KEY,
  dog_id INTEGER REFERENCES Dogs(id),
  show_id INTEGER REFERENCES Dog_shows(id),
  result INTEGER REFERENCES Championship_titles(id)
);

CREATE TABLE Litters (
  id INTEGER PRIMARY KEY,
  name TEXT UNIQUE,
  father_id TEXT REFERENCES Dogs(id),
  mother_id TEXT REFERENCES Dogs(id),
  date_of_birth DATE,
  owner_id INTEGER REFERENCES Owners(id)
);
