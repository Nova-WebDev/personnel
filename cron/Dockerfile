FROM alpine:3.19

RUN apk add --no-cache curl tzdata

COPY run.sh /usr/local/bin/run.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY crontab /etc/crontabs/root

RUN chmod +x /usr/local/bin/run.sh /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["crond", "-f", "-l", "2"]
