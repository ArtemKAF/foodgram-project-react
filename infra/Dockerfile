ARG NGINX_VERSION
FROM nginx:$NGINX_VERSION
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ../docs/ /usr/share/nginx/html/api/docs/
