# Use a lightweight and optimized Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only necessary files for dependency installation (uncomment if requirements.txt is available)
 COPY requirements.txt /app/

# Install required dependencies with no cache to minimize image size (uncomment if needed)

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY devops /app
RUN cd devops
# Set environment variables in modern format
ENV NAME=World
# Run the application      
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
