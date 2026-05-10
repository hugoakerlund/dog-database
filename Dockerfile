FROM ubuntu

EXPOSE 5000

WORKDIR /usr/src/app

COPY . .

RUN apt-get update && apt-get install -y python3 python3-flask sqlite3

RUN sqlite3 database.db < schema.sql

RUN python3 seed.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
