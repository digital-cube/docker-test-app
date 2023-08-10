#!/bin/sh

# Use sed to replace placeholders with environment variable values
sed -i "s/\${APP_HOST}/$APP_HOST/g" /etc/nginx/conf.d/default.conf

exec nginx -g 'daemon off;'