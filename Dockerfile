# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app/webapp.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]