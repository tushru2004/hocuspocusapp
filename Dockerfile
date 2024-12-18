# Use the official Python image based on Debian
FROM mitmproxy/mitmproxy:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY ./requirements.txt /app

# Upgrade pip and install dependencies
#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#RUN pip install mitmproxy

# Copy the rest of the application code
COPY ./src /app
COPY Makefile /app

# Expose the port that the application will listen on
EXPOSE 52233
ENV PYTHONUNBUFFERED=1

# Run the application
#ENTRYPOINT ["python3", "-u", "intercept.py"]
#ENTRYPOINT ["mitmdump", "-s", "/app/options.py"]
ENTRYPOINT ["mitmdump", "-s", "/app/anatomy.py", "--ignore-hosts", "^(.+\\.)?icloud\\.com:443$", "--ignore-hosts", "^(.+\\.)?apple\\.com:443$"]
