#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static.

# Update the package index files from their sources.
sudo apt-get update
# Install Nginx if it is not already installed, without any interactive prompts.
sudo apt-get -y install nginx

# Allow traffic on port 80 for Nginx HTTP through the firewall.
sudo ufw allow 'Nginx HTTP'

# Create the required directories if they do not exist.
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
# Create an empty index.html file in the test directory.
sudo touch /data/web_static/releases/test/index.html

# Populate the fake HTML file with simple content to test the Nginx configuration.
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link named 'current' to point to the test directory.
# If the symbolic link already exists, it will be overwritten (-f flag).
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Recursively change the ownership of the /data/ directory to the 'ubuntu' user and group.
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/
# under the alias /hbnb_static. This is done by inserting the configuration just after
# the 'listen 80 default_server;' directive in the default site configuration.
sudo sed -i '/listen 80 default_server;/a location /hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-available/default

# Restart Nginx to apply the new configuration.
sudo service nginx restart
