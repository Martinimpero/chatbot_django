# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]