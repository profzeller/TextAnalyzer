# Use the official Nginx image as a parent image
FROM nginx:alpine

# Copy your custom nginx.conf into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Optionally, set permissions and ownership
RUN chmod 644 /etc/nginx/nginx.conf && \
    chown nginx:nginx /etc/nginx/nginx.conf

# Use the `nginx` user to run the container
USER nginx
