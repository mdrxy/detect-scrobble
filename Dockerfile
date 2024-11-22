FROM python:3.9-slim
WORKDIR /app

# Copy only necessary files
COPY requirements.txt ./
COPY detect.py ./
COPY .env ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y cron

# Apply cron job and give execution rights
COPY crontab.txt /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob && crontab /etc/cron.d/cronjob

# Start cron in foreground
CMD ["cron", "-f"]