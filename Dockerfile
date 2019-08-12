FROM python:3.6.5

RUN pip3 install pipenv

COPY Pipfile /

RUN pipenv install --skip-lock

ENV FLASK_APP wsgi.py

COPY . /

CMD ["pipenv", "run", "gunicorn", "-w", "5", "-b", "0.0.0.0:80", "wsgi:app"]
