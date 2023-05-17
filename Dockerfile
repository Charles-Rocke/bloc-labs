# using a python 3.10 image
FROM python:3.8-alpine
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME
# what port being used
# the working directory
# copy requirements into current folder
COPY requirements.txt .
# what to run at the begining of the image
# copy contents from current directory
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# what commands should run when container starts
# CMD ["/bin/bash", "docker-entrypoint.sh"]
# configure the container to run in an executed manner
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app