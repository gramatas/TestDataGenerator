FROM python:3.8.0-slim

ENV PYTHONUNBUFFERED 1

RUN apt update \
  && apt -y install postgresql-client

RUN addgroup --system django
RUN adduser --system django

# Requirements are installed here to ensure they will be cached.
# Requirements are installed here to ensure they will be cached.
COPY ./inDataGen/requirements /requirements
RUN pip install -r /requirements/production.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./compose/production/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

COPY ./compose/production/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker
RUN chown django /start-celeryworker

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
