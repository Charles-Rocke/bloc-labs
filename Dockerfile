# using a python 3.10 image
FROM python:3.10
# what port being used
# the working directory
WORKDIR /app
# copy requirements into current folder
COPY requirements.txt .
# what to run at the begining of the image
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# copy contents from current directory
COPY . .
# what commands should run when container starts
CMD ["/bin/bash", "docker-entrypoint.sh"]