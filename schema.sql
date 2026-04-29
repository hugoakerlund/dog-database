PRAGMA foreign_keys = ON;

CREATE TABLE owners (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    email TEXT UNIQUE,
    password_hash TEXT,
    created_at DATE
);

CREATE TABLE dogs (
    id INTEGER PRIMARY KEY,
    registration_number TEXT UNIQUE,
    registration_date DATE,
    name TEXT,
    image BLOB,
    color TEXT REFERENCES colors(name) ON DELETE RESTRICT,
    breed TEXT REFERENCES dog_breeds(name) ON DELETE RESTRICT,
    date_of_birth DATE,
    date_of_death DATE,
    sex TEXT CHECK (sex IN ('Male', 'Female')),
    owner_id INTEGER REFERENCES owners(id) ON DELETE CASCADE,
    litter_id INTEGER REFERENCES Litters(id) ON DELETE SET NULL,
    best_test INTEGER CHECK (best_test IN (1, 2, 3, 4, 5)),
    best_show_id INTEGER REFERENCES dog_shows(id) ON DELETE SET NULL,
    hip_index INTEGER,
    use_index INTEGER
);

CREATE TABLE colors (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE championship_titles (
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
);

CREATE TABLE dog_breeds (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE dog_shows (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    winner_id INTEGER REFERENCES dogs(id),
    date DATE
);

CREATE TABLE show_participants (
    id INTEGER PRIMARY KEY,
    dog_id INTEGER REFERENCES dogs(id) ON DELETE CASCADE,
    show_id INTEGER REFERENCES dog_shows(id) ON DELETE CASCADE,
    result INTEGER REFERENCES championship_titles(id)
);

CREATE TABLE litters (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    father_id INTEGER REFERENCES dogs(id) ON DELETE SET NULL,
    mother_id INTEGER REFERENCES dogs(id) ON DELETE SET NULL,
    date_of_birth DATE,
    owner_id INTEGER REFERENCES owners(id) ON DELETE CASCADE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    owner_id INTEGER REFERENCES owners(id) ON DELETE CASCADE,
    dog_id INTEGER REFERENCES dogs(id) ON DELETE CASCADE,
    sent_at DATE
);

CREATE INDEX idx_dogs_owner_id ON dogs(owner_id);
CREATE INDEX idx_dogs_litter_id ON dogs(litter_id);
CREATE INDEX idx_dogs_best_show_id ON dogs(best_show_id);
CREATE INDEX idx_dogs_color ON dogs(color);
CREATE INDEX idx_dogs_breed ON dogs(breed);

CREATE INDEX idx_litters_father_id ON litters(father_id);
CREATE INDEX idx_litters_mother_id ON litters(mother_id);
CREATE INDEX idx_litters_owner_id ON litters(owner_id);
CREATE INDEX idx_litters_date_of_birth ON litters(date_of_birth DESC);

CREATE INDEX idx_dog_shows_winner_id ON dog_shows(winner_id);

CREATE INDEX idx_show_participants_show_id ON show_participants(show_id);
CREATE INDEX idx_show_participants_dog_id ON show_participants(dog_id);
CREATE INDEX idx_show_participants_result ON show_participants(result);

CREATE INDEX idx_comments_dog_id ON comments(dog_id);
CREATE INDEX idx_comments_owner_id ON comments(owner_id);
