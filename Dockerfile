# Use the official Python image as the base image
FROM python:3.8-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the container
COPY . .

# Expose the port that the app will listen on
EXPOSE 5000

# Set the entrypoint command to run the Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
