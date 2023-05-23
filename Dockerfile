# Use the official Python image as the base image
FROM python:3.8-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# check what is copied to the directory
RUN ls

# Set the Flask environment variables
ENV FLASK_APP=main.py

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY . .


# Expose the port that the app will listen on
EXPOSE 5000

