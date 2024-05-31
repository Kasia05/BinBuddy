# Use a specific version of Python runtime as a parent image
FROM python:3.10.6-buster

# Upgrade pip to the latest version
RUN pip install --upgrade pip

COPY binbuddy binbuddy

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# run the application locally
#CMD uvicorn binbuddy.api.api:app --host 0.0.0.0

# run the application locally
CMD uvicorn binbuddy.api.api:app --host 0.0.0.0 --port $PORT
