#!/bin/sh
printenv CRON_API_KEY > /etc/cron_api_key
chmod 600 /etc/cron_api_key
exec "$@"
