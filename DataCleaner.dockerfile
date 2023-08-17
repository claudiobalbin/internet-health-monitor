FROM python:3.11

# Install necessary packages
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Install python packages
COPY requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt

# Copy your script into the container
COPY data_cleaner.py /usr/local/bin/data_cleaner.py

# Give execute permissions to the script
RUN chmod +x /usr/local/bin/data_cleaner.py

# Add the cron job to the crontab file
RUN echo "*/5 * * * * /usr/bin/python /usr/local/bin/data_cleaner.py" >> /etc/cron.d/data_cleaner

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/data_cleaner

# Apply cron job
RUN crontab /etc/cron.d/data_cleaner

# Run cron in the foreground
CMD ["cron", "-f"]
