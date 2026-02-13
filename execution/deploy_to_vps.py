
import os
import zipfile
import paramiko
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SSH_STRING = os.getenv("SSH_ROOT") # Expected: ssh user@ip
VPS_PASSWORD = os.getenv("VPS_PASSWORD")
LOCAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE_DIR = "/root/audit-shopee"
ZIP_FILENAME = "app_deploy.zip"

def parse_ssh_string(ssh_str):
    """Parses 'ssh user@ip' into user and ip."""
    if not ssh_str:
        raise ValueError("SSH_ROOT environment variable not found.")
    parts = ssh_str.replace("ssh ", "").split("@")
    if len(parts) != 2:
        raise ValueError(f"Invalid SSH string format: {ssh_str}")
    return parts[0], parts[1]

def create_zip(source_dir, output_filename):
    """Zips the project files."""
    print(f"Zipping files from {source_dir} to {output_filename}...")
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            if '.git' in root or '.venv' in root or '__pycache__' in root or 'outputs' in root or '.tmp' in root:
                continue
            for file in files:
                if file == output_filename or file.endswith('.zip') or file.endswith('.pyc'):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                arcname = arcname.replace(os.sep, '/')
                zipf.write(file_path, arcname)
    print("Zip created.")

def deploy():
    try:
        user, host = parse_ssh_string(SSH_STRING)
        print(f"Deploying to {user}@{host}...")
        
        # Create zip
        zip_path = os.path.join(LOCAL_DIR, ZIP_FILENAME)
        create_zip(LOCAL_DIR, zip_path)
        
        # Connect SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=VPS_PASSWORD)
        
        # SFTP Upload
        sftp = ssh.open_sftp()
        try:
            sftp.mkdir(REMOTE_DIR)
        except OSError:
            pass 
        
        remote_zip = os.path.join(REMOTE_DIR, ZIP_FILENAME).replace("\\", "/") # Ensure forward slash
        print(f"Uploading {ZIP_FILENAME} to {remote_zip}...")
        sftp.put(zip_path, remote_zip)
        sftp.close()
        
        # Execute commands
        commands = [
            f"ls -l {remote_zip}",
            f"cd {REMOTE_DIR} && python3 -c \"import zipfile; zipfile.ZipFile('{remote_zip}', 'r').extractall('.')\"",
            f"cd {REMOTE_DIR} && mkdir -p outputs",
            f"cd {REMOTE_DIR} && (python3 -m venv venv || virtualenv venv)",
            f"cd {REMOTE_DIR} && ./venv/bin/pip install --upgrade pip",
            f"cd {REMOTE_DIR} && ./venv/bin/pip install flask jinja2",
            "pkill -f serve_report.py || true",
            f"cd {REMOTE_DIR} && nohup ./venv/bin/python execution/serve_report.py > server.log 2>&1 &"
        ]
        
        for cmd in commands:
            print(f"Executing: {cmd}")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            
            if "nohup" in cmd:
                time.sleep(2)
                print("Server started (presumably).")
            else:
                exit_status = stdout.channel.recv_exit_status()
                if exit_status != 0:
                    print(f"Error executing command: {cmd}")
                    print(stderr.read().decode())
                else:
                    print(stdout.read().decode())

        print("Deployment completed successfully!")
        
        time.sleep(3)
        stdin, stdout, stderr = ssh.exec_command("ps aux | grep serve_report")
        print("Process check:")
        print(stdout.read().decode())

        stdin, stdout, stderr = ssh.exec_command("netstat -tuln | grep 1101")
        print("Verifying port 1101:")
        print(stdout.read().decode())
        
        ssh.close()
        
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        print(f"App likely live at http://{host}:1101")

    except Exception as e:
        print(f"Deployment failed: {e}")

if __name__ == "__main__":
    deploy()
