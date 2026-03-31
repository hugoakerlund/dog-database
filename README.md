# Dog database

Dog database is a simple web application built with Flask that allows users to view and manage a collection of dogs. The application provides a user-friendly interface for displaying dog information, commenting on other users’ dogs, adding new dogs, and deleting existing dogs from the database. Users can also create litters with dogs they own and enter their dogs in dog shows. Dogs earn championship titles by participating in dog shows.

## App functions

* The user can create an account and login.
* The user can add, edit and delete dogs and litters.
* The user can add an image for the dog.
* The user can see the added dogs, litters and other users.
* The user can search dogs with a query.
* The app has a user page that shows the dogs and litters that the user owns.
* The user can choose one or more classifications for the dog (e.g. breed, color).
* The user can enter their dogs in a dog show. The entry list shows which dogs have entered.
* The user can comment on other users' dogs.

## Installation

Install `flask` with pip:

```
$ pip install flask
```

Create database tables and initial data:

```
$ sqlite3 database.db < schema.sql
$ python3 seed.py
```

Run app with:

```
$ flask run
```

app will be available at https://localhost:5000
