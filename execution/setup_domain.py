
import os
import paramiko
import time
from dotenv import load_dotenv

load_dotenv()

SSH_STRING = os.getenv("SSH_ROOT")
VPS_PASSWORD = os.getenv("VPS_PASSWORD")
DOMAIN = "audittoko.digivise.id"
EMAIL = "admin@digivise.id" # For Let's Encrypt
APP_PORT = 1101

def parse_ssh_string(ssh_str):
    if not ssh_str: raise ValueError("SSH_ROOT missing")
    parts = ssh_str.replace("ssh ", "").split("@")
    return parts[0], parts[1]

def setup_domain_ssl():
    try:
        user, host = parse_ssh_string(SSH_STRING)
        print(f"Connecting to {user}@{host}...")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=VPS_PASSWORD)
        
        def run_command(cmd, description):
            print(f"\n[STEP] {description}...")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            # Wait for command to complete and capture output
            exit_status = stdout.channel.recv_exit_status()
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            
            if exit_status != 0:
                print(f"FAILED: {cmd}")
                print(f"STDERR: {err}")
                raise Exception(f"Command failed: {description}")
            else:
                print("SUCCESS")
                if out: print(f"OUTPUT: {out[:200]}..." if len(out) > 200 else f"OUTPUT: {out}")

        # 1. Install Nginx and Certbot
        # Update first to ensure we get package versions
        run_command("apt-get update", "Updating package lists")
        run_command("apt-get install -y nginx certbot python3-certbot-nginx", "Installing Nginx and Certbot")

        # 2. Configure Nginx Reverse Proxy
        nginx_config = f"""
server {{
    server_name {DOMAIN};

    location / {{
        proxy_pass http://127.0.0.1:{APP_PORT};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}
"""
        # We start by writing a basic HTTP config, Certbot will upgrade it to HTTPS
        temp_config_path = f"/etc/nginx/sites-available/{DOMAIN}"
        
        # Use simple echo to write file (careful with quotes)
        # We'll upload the config via SFTP to be safe
        sftp = ssh.open_sftp()
        with sftp.file(f"/tmp/{DOMAIN}", "w") as f:
            f.write(nginx_config)
        sftp.close()
        
        run_command(f"mv /tmp/{DOMAIN} {temp_config_path}", "Moving Nginx config to sites-available")
        
        # Enable site
        run_command(f"ln -sf {temp_config_path} /etc/nginx/sites-enabled/", "Enabling Nginx site")
        
        # Remove default if it exists (optional, but good to avoid conflicts if default catches all)
        # run_command("rm -f /etc/nginx/sites-enabled/default", "Removing default Nginx site")
        
        run_command("nginx -t", "Testing Nginx configuration")
        run_command("systemctl reload nginx", "Reloading Nginx")

        # 3. Obtain SSL Certificate
        # --non-interactive: Run without asking for user input
        # --agree-tos: Agree to Terms of Service
        # -m: Email for urgent notices
        # --redirect: Force redirect HTTP to HTTPS
        certbot_cmd = f"certbot --nginx -d {DOMAIN} --non-interactive --agree-tos -m {EMAIL} --redirect"
        run_command(certbot_cmd, "Obtaining SSL Certificate via Certbot")

        print(f"\n✅ SETUP COMPLETE!")
        print(f"URL: https://{DOMAIN}")
        
        ssh.close()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    setup_domain_ssl()
