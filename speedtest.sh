#!/bin/bash
current_time=$(date "+%Y%m%d-%H%M%S")
file_name=$current_time.json

speedtest --json >> /logger_output/$file_name
