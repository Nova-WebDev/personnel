FROM nginx:stable

RUN rm -f /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf
COPY dist /usr/share/nginx/html

