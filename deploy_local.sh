#!/bin/bash
# Quick local deployment for testing

echo "Deploying AfriBnB web_static locally..."

# Create the data directory if it doesn't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Copy your web_static files
sudo cp -r web_static/* /data/web_static/releases/test/

# Create/update the symbolic link
sudo rm -rf /data/web_static/current
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Set correct permissions
sudo chown -R $USER:$USER /data/web_static

echo "Deployment complete!"
echo "Your files are at: /data/web_static/current/"
ls -la /data/web_static/current/