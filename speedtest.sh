#!/bin/bash
current_time=$(date "+%Y%m%d-%H%M%S")
file_name=$current_time.json

speedtest --json >> /tmp/$file_name
mv /tmp/$file_name /logger_output/$file_name
echo "Log generated at $current_time"
