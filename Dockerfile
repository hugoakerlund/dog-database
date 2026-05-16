FROM python:3.12-alpine

EXPOSE 5000

WORKDIR /usr/src/app

RUN apk add --no-cache sqlite

RUN pip install --no-cache-dir MarkupSafe Flask

COPY . .

RUN sqlite3 database.db < schema.sql && \
    python3 seed.py && \
    rm -rf /root/.cache /tmp/* && \
    adduser -D appuser && \
    chown -R appuser:appuser /usr/src/app

USER appuser

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
