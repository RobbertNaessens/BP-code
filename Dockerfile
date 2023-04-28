# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR .

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
RUN mkdir /app
COPY . /app

# Run the command to start the main.py file
CMD ["python", "/app/main.py"]
