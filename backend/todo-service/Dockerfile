# 1. Use an official modern Python runtime as a parent image
FROM python:3.12-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set the working directory
WORKDIR /app

# 4. Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the project code
COPY . .

COPY start.sh /start.sh
RUN chmod +x /start.sh

# The command to run the application
CMD ["/start.sh"]