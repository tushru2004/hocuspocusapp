# Use the official Python image based on Debian
FROM python:3.11-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip
# Install the dependencies
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Expose the port that the application will listen on
EXPOSE 52233

# Run the application
ENTRYPOINT ["python3", "-u", "intercept.py"]
