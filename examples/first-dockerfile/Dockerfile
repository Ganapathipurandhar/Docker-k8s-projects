# Use the latest Ubuntu image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install the necessary packages
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install docker

# Set environment variables (optional, can be removed if not used)
ENV NAME World

# Default command to run the Python script
CMD ["python3", "get_logs.py"]
