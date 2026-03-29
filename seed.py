import os
import random
import string
import db
from app import app

colors = [
'Brown', 
'Chocolate', 
'Liver',
'Red',
'Gold',
'Yellow',
'Cream',
'Fawn',
'Black',
'Blue',
'Gray',
'Silver',
'White']

dog_breeds = [
'Affenpinscher',
'Afghan Hound',
'Africanis',
'Aidi',
'Airedale Terrier',
'Akbash',
'Akita',
'Aksaray Malaklisi',
'Alano Español',
'Alapaha Blue Blood Bulldog',
'Alaskan Husky',
'Alaskan Klee Kai',
'Alaskan Malamute',
'Alopekis',
'Alpine Dachsbracke',
'American Bulldog',
'American Bully',
'American Cocker Spaniel',
'American English Coonhound',
'American Eskimo Dog',
'Finnish Spitz']

dog_names = [
'Max',
'Charlie',
'Bella',
'Poppy',
'Daisy',
'Buster',
'Alfie',
'Millie',
'Molly',
'Rosie',
'Buddy',
'Barney',
'Lola',
'Roxy',
'Ruby',
'Tilly',
'Bailey',
'Marley',
'Tia',
'Bonnie',
'Toby',
'Milo',
'Archie',
'Holly',
'Lucy']

dog_shows = [
('Spring Dog Show', '2024-03-15'),
('Summer Dog Show', '2024-06-20'),
('Autumn Dog Show', '2024-09-10'),
('Winter Dog Show', '2024-12-05')]

championship_titles = [
"None", # No title
"Exc", # Excellent
"VG", # Very Good
"G", # Good
"S", # Sufficient
"VP", # Very Promising
"P", # Promising
"Puppy BOB", # Puppy Best of Breed
"J CAC", # Junior Certificate of Aptitude for the Beauty Championship
"J CACIB", # Junior Certificate of Aptitude for the International Beauty Championship
"J BOB", # Junior Best of Breed
"CAC", # Certificate of Championship Aptitude
"CACIB", # Certificate of Aptitude for the International Beauty Championship
"BOB", # Best of Breed
"BOS", # Best Opposite Sex - optional
"V CAC", # Veteran Certificate of Aptitude:
"V CACIB", # Veteran Certificate of Aptitude International:
"V BOB", # Veteran Best of Breed
"V BOS", # Veteran Best Opposite Sex - optional
"BOG", # Best of Group
"J BIS", # Junior Best in Show
"BIS", # Best in Show
]

pictures = os.listdir('static/pictures')

def create_random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))

def create_random_date():
        year = random.randint(2000, 2024)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return f"{year}-{month:02d}-{day:02d}"

def insert_random_owner(id):
        name = "test_owner" + str(id)
        email = name + "@" + "test_domain" + ".com"
        password_hash = "test_hash"
        sql = "INSERT INTO Owners (name, email, password_hash) VALUES (?, ?, ?)"
        db.execute(sql, [name, email, password_hash])

def create_litter(id, father_id, mother_id):
        name = "test_litter" + str(id)
        date_of_birth = create_random_date()
        sql = "INSERT INTO Litters (id, name, father_id, mother_id, date_of_birth, owner_id) VALUES (?, ?, ?, ?, ?, ?)"
        db.execute(sql, [id, name, father_id, mother_id, date_of_birth, id])


def insert_random_dog(id):
        year = f"{id:04}"
        registration_number = "FI" + f"{id:05}" + "/" + year[2:]
        name = random.choice(dog_names)
        image = random.choice(pictures)
        color = random.choice(colors)
        breed = random.choice(dog_breeds)
        date_of_birth = create_random_date()
        sex = random.choice(["Male", "Female"])

        father_id = random.randint(1, id - 1) if id > 2 else None
        mother_id = random.randint(1, id - 1) if id > 2 else None
        litter_id = None
        if father_id and mother_id:
            create_litter(id, father_id, mother_id)
            litter_id = id

        owner_id = id
        best_test = random.randint(1,5)
        best_show_id = random.randint(1, len(dog_shows) - 1)
        hip_index = random.randint(0,100)
        use_index = random.randint(0,100)

        sql = """INSERT INTO Dogs (registration_number, name, image, color, breed, date_of_birth, 
                                   sex, owner_id, litter_id, 
                                   best_test, best_show_id, hip_index, use_index) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        db.execute(sql, [registration_number, name, image, color, breed, date_of_birth, 
                                sex, owner_id, litter_id, best_test, best_show_id, hip_index, use_index])

def seed_table_colors():
     sql = "INSERT INTO Colors (name) VALUES (?)"
     for i in range(len(colors)):
          color = colors[i]
          db.execute(sql, [color])
    
def seed_table_dog_shows():
     sql = "INSERT INTO Dog_shows (name, date) VALUES (?,?)"
     for i in range(len(dog_shows)):
          name = dog_shows[i][0]
          date = dog_shows[i][1]
          db.execute(sql, [name, date])

def seed_table_dog_breeds():
      sql = "INSERT INTO Dog_breeds (name) VALUES (?)"
      for i in range(len(dog_breeds)):
        breed = dog_breeds[i]
        db.execute(sql, [breed])
    
def seed_table_championship_titles():
      sql = "INSERT INTO Championship_titles (title) VALUES (?)"
      for i in range(len(championship_titles)):
        title = championship_titles[i]
        db.execute(sql, [title])

def insert_show_participant(id):
      sql = "INSERT INTO Show_participants (dog_id, show_id, result) VALUES (?,?,?)"
      dog_id = id
      show_id = random.randint(1, len(dog_shows))
      result = random.randint(1, len(championship_titles))
      db.execute(sql, [dog_id, show_id, result])

def set_show_winner(show_id, dog_id):
      sql = "UPDATE Dog_shows SET winner_id = ? WHERE id = ?"
      db.execute(sql, [dog_id, show_id])

with app.app_context():
    n = 100
    seed_table_colors()
    seed_table_dog_breeds()
    seed_table_dog_shows()
    seed_table_championship_titles()

    for id in range(1, n):
        insert_random_owner(id)
        insert_random_dog(id)
        insert_show_participant(id)

    for show_id in range(1, len(dog_shows) + 1):
        winner_id = random.randint(1, n - 1)
        set_show_winner(show_id, winner_id)
