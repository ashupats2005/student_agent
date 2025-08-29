FROM python:3.12-slim

WORKDIR /app

# Copy all project files
COPY . /app

# Install dependencies including flask-cors
RUN pip install flask requests flask-cors

# Expose Flask port
EXPOSE 5001

# Run registration.py in background & Flask app in foreground
CMD ["sh", "-c", "python registration.py & python student_agent.py"]
