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

## Performance-report

Test data was created with `seed.py`.

`DOG_COUNT` was set to `10**6`.


Code was added for printing request times:

```
import time
from flask import g

...

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

```

The app generally performs quickly with large amounts of data. Here are some examples of request times:

### Loading page `/`
```
elapsed time: 0.03 s
127.0.0.1 - - [27/Apr/2026 18:52:35] "GET / HTTP/1.1" 200 -
elapsed time: 0.01 s
127.0.0.1 - - [27/Apr/2026 18:52:35] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [27/Apr/2026 18:53:38] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:53:38] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [27/Apr/2026 18:53:40] "GET /3 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:53:40] "GET /static/style.css HTTP/1.1" 304 -
```

### Loading page `/litters`
```
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 19:09:02] "GET /litters HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:09:03] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 19:09:04] "GET /litters/2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:09:04] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [27/Apr/2026 19:09:06] "GET /litters/3 HTTP/1.1" 200 -

```

### Loading page `/owners`
```
elapsed time: 0.04 s
127.0.0.1 - - [27/Apr/2026 18:55:35] "GET /owners HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:55:35] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 18:55:37] "GET /owners/2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:55:37] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [27/Apr/2026 18:55:38] "GET /owners/3 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:55:38] "GET /static/style.css HTTP/1.1" 304 -
```

### Loading page `/dog_shows`
```
elapsed time: 0.01 s
127.0.0.1 - - [27/Apr/2026 19:24:25] "GET /dog_shows HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:24:26] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [27/Apr/2026 19:24:27] "GET /dog_show/4 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:24:27] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 19:24:30] "GET /dog_show/4/2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:24:30] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 19:24:30] "GET /dog_show/4/3 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:24:30] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 19:24:31] "GET /dog_show/4/4 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:24:31] "GET /static/style.css HTTP/1.1" 304 -
```

### Searching
```
elapsed time: 0.2 s
127.0.0.1 - - [27/Apr/2026 18:54:37] "GET /search?query=a HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:54:37] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.21 s
127.0.0.1 - - [27/Apr/2026 18:54:46] "GET /search/2?query=a HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:54:46] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.24 s
127.0.0.1 - - [27/Apr/2026 18:54:48] "GET /search/3?query=a HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:54:48] "GET /static/style.css HTTP/1.1" 304 -

```

### Creating an account
```
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:57:11] "GET /register HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:57:11] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.18 s
127.0.0.1 - - [27/Apr/2026 18:57:20] "POST /register HTTP/1.1" 302 -
elapsed time: 0.01 s
127.0.0.1 - - [27/Apr/2026 18:57:20] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:57:20] "GET /static/style.css HTTP/1.1" 304 -
```

### Removing an account
```
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:55:44] "GET /owner/1000000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:55:44] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:57:04] "GET /owner/1000000/remove HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:57:04] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.17 s
127.0.0.1 - - [27/Apr/2026 19:57:06] "POST /owner/1000000/remove HTTP/1.1" 302 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 19:57:06] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:57:06] "GET /static/style.css HTTP/1.1" 304 -

```

### Adding a dog

```
elapsed time: 0.04 s
127.0.0.1 - - [27/Apr/2026 18:57:52] "GET /dog/new HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:57:52] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.11 s
127.0.0.1 - - [27/Apr/2026 18:58:04] "POST /dog/new HTTP/1.1" 302 -
elapsed time: 0.02 s
127.0.0.1 - - [27/Apr/2026 18:58:04] "GET /owner/1000000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:58:05] "GET /static/style.css HTTP/1.1" 304 -
```

### Removing a dog
```
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:55:42] "GET /dog/1000000/remove HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:55:42] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.28 s
127.0.0.1 - - [27/Apr/2026 19:55:44] "POST /dog/1000000/remove HTTP/1.1" 302 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:55:44] "GET /owner/1000000 HTTP/1.1" 200 -
```

### Adding a comment
```
elapsed time: 0.15 s
127.0.0.1 - - [27/Apr/2026 19:59:15] "POST /comment/new HTTP/1.1" 302 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:59:15] "GET /dog/1000000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:59:15] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:59:15] "GET /image/1000000 HTTP/1.1" 200 -
```


### Adding a litter
```
elapsed time: 0.04 s
127.0.0.1 - - [27/Apr/2026 18:58:47] "GET /litter/new HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:58:48] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.09 s
127.0.0.1 - - [27/Apr/2026 18:58:53] "POST /litter/new HTTP/1.1" 302 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:58:53] "GET /owner/1000000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:58:54] "GET /static/style.css HTTP/1.1" 304 -
```

### Removing a litter
```
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:59:19] "GET /litter/1000000/remove HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:59:19] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.08 s
127.0.0.1 - - [27/Apr/2026 18:59:20] "POST /litter/1000000/remove HTTP/1.1" 302 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:59:20] "GET /owner/1000000 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 18:59:21] "GET /static/style.css HTTP/1.1" 304
```

### Adding a dog to a dog show
```
elapsed time: 0.1 s
127.0.0.1 - - [27/Apr/2026 19:55:00] "POST /dog_show/4/add HTTP/1.1" 302 -
elapsed time: 0.17 s
127.0.0.1 - - [27/Apr/2026 19:55:00] "GET /dog_show/4 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:55:00] "GET /static/style.css HTTP/1.1" 304 -
```

### Removing a dog from a dog show
```
elapsed time: 0.1 s
127.0.0.1 - - [27/Apr/2026 19:55:15] "POST /dog_show/4/remove HTTP/1.1" 302 -
elapsed time: 0.17 s
127.0.0.1 - - [27/Apr/2026 19:55:15] "GET /dog_show/4 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [27/Apr/2026 19:55:15] "GET /static/style.css HTTP/1.1" 304 -
```
