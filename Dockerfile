FROM python:3.11

WORKDIR /projects

COPY Pipfile Pipfile.lock /projects/
COPY requirements.txt /projects/

RUN pip install -r requirements.txt

RUN pip install pipenv && pipenv install --system --deploy

COPY . /projects/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000
