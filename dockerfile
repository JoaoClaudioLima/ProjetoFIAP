# Use Python 3.12 as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install pymongo (MongoDB driver for Python)
RUN pip install --no-cache-dir pymongo

# Install any other dependencies you may have in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Command to run on container start
CMD ["python", "app.py"]