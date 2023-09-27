# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script and requirements.txt into the container
COPY ./data_prep.py .
COPY ./requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for the data output
RUN mkdir -p src/data

# CMD instruction to run the script when the container launches
CMD ["python", "./data_prep.py"]