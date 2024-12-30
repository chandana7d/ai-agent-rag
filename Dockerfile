# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .
COPY main.py . 
COPY .env . 
COPY index_data.py .


# Install the dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY src/ src/

RUN mkdir -p /app/db_data


# Command to run the application using Uvicorn
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
