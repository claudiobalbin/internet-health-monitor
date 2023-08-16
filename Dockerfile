FROM  alpine:3.18

RUN apk add speedtest-cli

ADD speedtest.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/speedtest.sh

# Starts the test script every 5 minutes
RUN echo '*/5  *  *  *  *  /bin/ash /usr/local/bin/speedtest.sh' > /etc/crontabs/root

# Sets crond log level and to run in foreground
CMD ["crond", "-l", "2", "-f"]
