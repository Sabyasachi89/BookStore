FROM python:3.9.16-slim

ADD ./app /usr/src/app/app
ADD ./db /usr/src/app/db
ADD ./helm /usr/src/app/helm
ADD ./Pipfile /usr/src/app/
ADD ./Pipfile.lock /usr/src/app/


ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
WORKDIR /usr/src/app/

RUN apt update && apt upgrade -y \
    && apt install -y lsb-release build-essential curl gnupg2 \
    && curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' \
    && apt install -y postgresql-client-13 \
    && apt-get -y install libpq-dev gcc \
    && apt clean \
    && pip install -U pip==22.3.1 \
    && pip install pipenv==2022.10.12 \
    && pipenv install

ENTRYPOINT ["pipenv", "run"]
CMD ["uvicorn", "app.src.main:app", "--reload", "--port=8000", "--host=0.0.0.0"]
