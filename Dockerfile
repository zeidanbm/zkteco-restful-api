# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy .env.production to .env
COPY .env.production .env

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install production-ready server like Gunicorn (Green Unicorn)
RUN pip install gunicorn

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the app with Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:80", "run:app"]