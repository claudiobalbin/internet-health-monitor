# Use the Debian as the base image
FROM python:3.10-bullseye

# Install required packages (Python, cron)
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy your Python script into the container
COPY data_cleaner.py /home/data_cleaner.py

# Install Python packages
RUN pip3 install peewee psycopg2 psycopg2-binary

# Give execute permissions to the script
RUN chmod +x /home/data_cleaner.py

# Add the cron job to the crontab file
RUN echo "*/5 * * * * /usr/local/bin/python3 /home/data_cleaner.py >> /proc/1/fd/1 2>&1" >> /etc/cron.d/data_cleaner

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/data_cleaner

# Apply cron job
RUN crontab /etc/cron.d/data_cleaner

# Run cron in the foreground
CMD ["cron", "-f", "-l", "2"]
