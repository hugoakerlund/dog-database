INSERT INTO Users (username, email, password_hash) VALUES
  ('Alice', 'alice.example.com', 'testhash1'),
  ('Bob', 'bob.example.com', 'testhash2'),
  ('Charlie', 'charlie.example.com', 'testhash3'),
  ('Danny', 'danny.example.com', 'testhash4'),
  ('Edward', 'edward.example.com', 'testhash5'),
  ('Frank', 'frank.example.com', 'testhash6'),
  ('Grant', 'grant.example.com', 'testhash7'),
  ('Hank', 'hank.example.com', 'testhash8'),
  ('Iris', 'iris.example.com', 'testhash9'),
  ('Jack', 'jack.example.com', 'testhash10');

INSERT INTO DogBreeds (name) VALUES
    ('Affenpinscher'),
    ('Afghan Hound'),
    ('Africanis'),
    ('Aidi'),
    ('Airedale Terrier'),
    ('Akbash'),
    ('Akita'),
    ('Aksaray Malaklisi'),
    ('Alano Español'),
    ('Alapaha Blue Blood Bulldog'),
    ('Alaskan Husky'),
    ('Alaskan Klee Kai'),
    ('Alaskan Malamute'),
    ('Alopekis'),
    ('Alpine Dachsbracke'),
    ('American Bulldog'),
    ('American Bully'),
    ('American Cocker Spaniel'),
    ('American English Coonhound'),
    ('American Eskimo Dog'),
    ('Finnish Spitz');

INSERT INTO DogShows (name, date) VALUES
    ('Spring Dog Show', '2024-03-15'),
    ('Summer Dog Show', '2024-06-20'),
    ('Autumn Dog Show', '2024-09-10'),
    ('Winter Dog Show', '2024-12-05');

INSERT INTO Dogs (registration_number, name, color, breed, born_date, sex, father_id, mother_id, owner_id, litters, championship_title, best_test, best_show, litter_score, score_trace, hip_index, use_index) VALUES
    ('FI28691/21', 'Dolly', 'Red', 'Finnish Spitz', '2020-01-01', 'M', NULL, NULL, 1, NULL, 'KVA', 1, 'Spring Dog Show', 'A+', 'Trace1', 85, 90),
    ('FI28692/21', 'Bella', 'White', 'Afghan Hound', '2019-05-10', 'F', NULL, NULL, 2, NULL, 'KV', 2, 'Summer Dog Show', 'A', 'Trace2', 80, 85),
    ('FI28693/21', 'Charlie', 'Brown', 'Africanis', '2021-03-20', 'M', NULL, NULL, 3, NULL, 'KVA2', 3, 'Autumn Dog Show', 'B+', 'Trace3', 75, 80),
    ('FI28694/21', 'Daisy', 'Yellow', 'Aidi', '2018-07-15', 'F', NULL, NULL, 4, NULL, 'KV2', 4, 'Winter Dog Show', 'B', 'Trace4', 70, 75),
    ('FI28695/21', 'Max', 'Gold', 'Airedale Terrier', '2020-11-30', 'M', NULL, NULL, 5, NULL, 'KVA3', 5, 'Spring Dog Show', 'C+', 'Trace5', 65, 70);

INSERT INTO Litters (father_id, mother_id, born_date) VALUES
    ('FI28692/21', 'FI28691/21', '2022-01-01'),
    ('FI28693/21', 'FI28694/21', '2023-02-15'),
    ('FI28695/21', 'FI28692/21', '2024-03-10');

INSERT INTO Pictures (dog_id, url) VALUES
    (1, 'https://commons.wikimedia.org/wiki/Suomenpystykorva#/media/File:Finnish_Spitz_600.jpg'),
    (2, 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Biju2005a.jpg/640px-Biju2005a.jpg'),
    (3, 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Africanis_4.jpg/640px-Africanis_4.jpg'),
    (4, 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Aidi.jpg/640px-Aidi.jpg'),
    (5, 'https://upload.wikimedia.org/wikipedia/commons/f/f4/Airedale_terrier_in_B%C4%99dzin%2C_Silesian_Voivodeship%2C_Poland%2C_October_2024.jpg');
