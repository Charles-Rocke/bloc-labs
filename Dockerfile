# pull official base image
FROM python:3.8.12-alpine As builder
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# install dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install gcc
RUN pip install --upgrade pip
RUN pip install pipenv
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./Pipfile /usr/src/app/Pipfile

# RUN pipenv install -e --skip-lock --system --dev
# copy project
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app