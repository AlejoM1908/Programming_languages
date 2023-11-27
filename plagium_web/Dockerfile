FROM nginx:alpine3.18

# Copy the HTML, CSS and JS files to the nginx directory
COPY ./ /usr/share/nginx/html

EXPOSE 80

# Run the nginx server
CMD ["nginx", "-g", "daemon off;"]