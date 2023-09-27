# Use an official Python runtime as the base image
FROM python:3.10-slim

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script, requirements.txt, and the start script into the container
COPY ./data_prep.py .
COPY ./requirements.txt .
COPY ./start.sh .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make the start.sh script executable
RUN chmod +x start.sh

# Create a directory for the data output
RUN mkdir -p src/data

# Add a cron job to run the Python script every day at 4 a.m.
RUN echo "* * * * * python /usr/src/app/data_prep.py >> /var/log/cron.log 2>&1" | crontab -

# Use the start.sh script as the command to run on startup
CMD ["./start.sh"]
