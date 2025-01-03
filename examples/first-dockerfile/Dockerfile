# Use a more lightweight and optimized Python image as the base image
FROM python:3.10-slim

# Set the working directory in the image
WORKDIR /app

# Copy only the necessary files to the image
#COPY requirements.txt /app/

# Install the required dependencies in a single layer
#RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Set environment variables
ENV NAME World

# Run the application
CMD ["python", "app.py"]
