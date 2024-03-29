# Use the official Nginx image as a base
FROM nginx:alpine

# Remove the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom nginx.conf into the container
COPY nginx.conf /etc/nginx/nginx.conf

# Optionally, adjust permissions and set the correct ownership
# Note: The 'nginx' user and group already exist in the nginx:alpine image
RUN chmod 644 /etc/nginx/nginx.conf && \
    chown nginx:nginx /etc/nginx/nginx.conf

# Switch to the 'nginx' user to run the Nginx server
USER nginx
