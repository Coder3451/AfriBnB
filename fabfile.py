#!/usr/bin/python3
from fabric.api import local, env, run, put, sudo
from datetime import datetime
import os

# YOUR SERVER IP
env.user = "segni"
env.hosts = ["192.168.136.56"]
env.password = "segniubuntu"

def do_pack():
    """Generate .tgz archive"""
    local("mkdir -p versions")
    now = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second
    )
    archive_path = "versions/{}".format(archive_name)
    local("tar -czvf {} web_static".format(archive_path))
    print("✅ Packed: {}".format(archive_path))
    return archive_path

def do_deploy(archive_path):
    """Deploy to server"""
    if not os.path.exists(archive_path):
        return False
    
    try:
        archive_file = archive_path.split('/')[-1]
        archive_name = archive_file.split('.')[0]
        release_path = "/data/web_static/releases/{}".format(archive_name)
        
        # Upload and deploy
        put(archive_path, "/tmp/{}".format(archive_file))
        sudo("mkdir -p {}".format(release_path))
        sudo("tar -xzf /tmp/{} -C {}".format(archive_file, release_path))
        sudo("rm /tmp/{}".format(archive_file))
        sudo("mv {}/web_static/* {}".format(release_path, release_path))
        sudo("rm -rf {}/web_static".format(release_path))
        sudo("rm -rf /data/web_static/current")
        sudo("ln -s {} /data/web_static/current".format(release_path))
        
        print("✅ Deployed to: {}".format(release_path))
        return True
    except Exception as e:
        print("❌ Failed: {}".format(e))
        return False

def deploy():
    """Full deploy"""
    archive = do_pack()
    if archive:
        return do_deploy(archive)
    return False

def setup_server():
    """Initial server setup"""
    try:
        # Install Nginx
        sudo("apt-get update -y")
        sudo("apt-get install -y nginx")
        
        # Create directories
        sudo("mkdir -p /data/web_static/releases/test")
        sudo("mkdir -p /data/web_static/shared")
        
        # Create test page
        run("echo '<h1>AfriBnB - Home Africa!</h1>' | sudo tee /data/web_static/releases/test/index.html")
        
        # Setup Nginx config
        nginx_config = '''server {
    listen 80;
    server_name _;
    
    location /afribnb/ {
        alias /data/web_static/current/;
        index index.html;
    }
    
    location / {
        return 200 "AfriBnB Running!";
        add_header Content-Type text/plain;
    }
}'''
        run("echo '{}' | sudo tee /etc/nginx/sites-available/default".format(nginx_config))
        
        # Restart Nginx
        sudo("service nginx restart")
        sudo("chown -R segni:segni /data")
        
        print("✅ Server setup complete!")
        return True
    except Exception as e:
        print("❌ Setup failed: {}".format(e))
        return False
