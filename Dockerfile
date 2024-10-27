# Use an official Python runtime as the base image
FROM python:3.9.13-alpine

# Maintainer
LABEL maintainer="ashrujit.pal@infosys.com"

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 8080

# Define Entrypoint
ENTRYPOINT ["python"]

# Define CMD
CMD ["src/app.py"]