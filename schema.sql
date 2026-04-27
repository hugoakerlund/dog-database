CREATE TABLE Owners (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT,
    created_at DATE
);

CREATE TABLE Dogs (
    id INTEGER PRIMARY KEY,
    registration_number TEXT UNIQUE,
    registration_date DATE,
    name TEXT,
    image BLOB,
    color TEXT REFERENCES Colors(name),
    breed TEXT REFERENCES Dog_breeds(name),
    date_of_birth DATE,
    date_of_death DATE,
    sex TEXT CHECK (sex IN ('Male', 'Female')),
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

CREATE TABLE Comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    owner_id INTEGER REFERENCES Owners(id),
    dog_id INTEGER REFERENCES Dogs(id),
    sent_at DATE
);

CREATE INDEX idx_dogs_owner_id ON Dogs(owner_id);
CREATE INDEX idx_dogs_litter_id ON Dogs(litter_id);
CREATE INDEX idx_dogs_best_show_id ON Dogs(best_show_id);
CREATE INDEX idx_dogs_color ON Dogs(color);
CREATE INDEX idx_dogs_breed ON Dogs(breed);

CREATE INDEX idx_litters_father_id ON Litters(father_id);
CREATE INDEX idx_litters_mother_id ON Litters(mother_id);
CREATE INDEX idx_litters_owner_id ON Litters(owner_id);
CREATE INDEX idx_litters_date_of_birth ON Litters(date_of_birth DESC);

CREATE INDEX idx_dog_shows_winner_id ON Dog_shows(winner_id);

CREATE INDEX idx_show_participants_show_id ON Show_participants(show_id);
CREATE INDEX idx_show_participants_dog_id ON Show_participants(dog_id);
CREATE INDEX idx_show_participants_result ON Show_participants(result);

CREATE INDEX idx_comments_dog_id ON Comments(dog_id);
CREATE INDEX idx_comments_owner_id ON Comments(owner_id);
