#!/bin/sh

# Run the Python script on startup
python /usr/src/app/data_prep.py

# Start the cron daemon in the foreground
exec cron -f