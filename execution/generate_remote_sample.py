
import os
import paramiko
from dotenv import load_dotenv

load_dotenv()

SSH_STRING = os.getenv("SSH_ROOT")
VPS_PASSWORD = os.getenv("VPS_PASSWORD")

def parse_ssh_string(ssh_str):
    if not ssh_str: raise ValueError("SSH_ROOT missing")
    parts = ssh_str.replace("ssh ", "").split("@")
    return parts[0], parts[1]

def generate_remote():
    try:
        user, host = parse_ssh_string(SSH_STRING)
        print(f"Connecting to {user}@{host}...")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=VPS_PASSWORD)
        
        # 1. Upload updated script
        sftp = ssh.open_sftp()
        local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'create_audit_report.py')
        remote_path = '/root/audit-shopee/execution/create_audit_report.py'
        
        print(f"Uploading {local_path} to {remote_path}...")
        sftp.put(local_path, remote_path)
        
        # 1b. Upload updated template
        local_tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'report_template.html')
        remote_tpl = '/root/audit-shopee/execution/templates/report_template.html'
        print(f"Uploading {local_tpl} to {remote_tpl}...")
        sftp.put(local_tpl, remote_tpl)
        
        sftp.close()

        # 2. Run generation script using the venv python
        cmd = "cd /root/audit-shopee && ./venv/bin/python execution/create_audit_report.py"
        print(f"Executing: {cmd}")
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stdout.read().decode())
        err = stderr.read().decode()
        if err: print(f"STDERR: {err}")
        
        ssh.close()
        print("Remote generation triggered.")
        print("View report at: http://audittoko.digivise.id:1101")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    generate_remote()
