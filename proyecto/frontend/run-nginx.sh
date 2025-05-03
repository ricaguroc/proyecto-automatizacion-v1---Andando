#!/bin/bash
podman run -d --name nginxtest \
	-v $(pwd)/html/:/usr/share/nginx/html:ro,Z \
	-v $(pwd)/config/nginx.conf:/etc/nginx/nginx.conf:ro,Z \
	-v $(pwd)/mime.types:/etc/nginx/mime.types:ro,Z \
	-p 8081:80 \
	nginx
