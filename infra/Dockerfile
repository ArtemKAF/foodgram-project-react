ARG NGINX_VERSION
FROM nginx:$NGINX_VERSION
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=docs redoc.html /usr/share/nginx/html/api/docs/
