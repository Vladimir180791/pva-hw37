FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create logs directory
RUN mkdir -p logs reports/allure-results

# Set environment variables
ENV PYTHONPATH=/app

# Command to run tests
CMD ["pytest", "tests/", "--alluredir=reports/allure-results"]