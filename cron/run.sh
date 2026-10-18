#!/bin/sh
curl -sS -f -X POST \
  -H "X-Api-Key: $(cat /etc/cron_api_key)" \
  http://backend:8000/meals/cron/meal-plan-recurring
