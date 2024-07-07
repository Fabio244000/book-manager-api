# Dockerfile
FROM ubuntu:20.04

ENV PYTHONUNBUFFERED=1

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y python3-pip python3-dev && \
    apt-get clean

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Command to run the application
CMD ["python3", "book_manager/manage.py", "runserver", "0.0.0.0:8000"]
