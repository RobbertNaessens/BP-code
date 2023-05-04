# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR .

# Copy the requirements file into the container and install dependencies
COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
RUN mkdir /app
COPY . /app

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Run the command to start the main.py file
CMD ["python", "/app/main.py"]

# Gebruikte commando's:

# docker build -t my_bp_image . => maak een nieuwe image aan met de naam 'my_bp_image'
# docker run --name web my_bp_image => run de image in een container met de naam 'web'
# docker tag my_bp_image robbertnaessens/my_bp_image => image taggen om dan te kunnen deployen naar docker hub
# docker login => inloggen op docker
# docker push robbertnaessens/my_bp_image => image pushen naar dockerhub
# docker pull robbertnaessens/my_bp_image => image pullen vanaf een ander device
# docker run --name web robbertnaessens/my_bp_image => run de image in een container met de naam 'web'

