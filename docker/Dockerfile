# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
#COPY requirements.txt .

# Install the dependencies
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir  fastapi uvicorn sqlalchemy asyncpg


# Copy the current directory contents into the container at /app
COPY . .

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the FastAPI app using uvicorn
# Command to run the application with uvicorn
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]