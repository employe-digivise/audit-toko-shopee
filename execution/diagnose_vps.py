
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

def diagnose():
    try:
        user, host = parse_ssh_string(SSH_STRING)
        print(f"Diagnosing {user}@{host}...")
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user, password=VPS_PASSWORD)
        
        cmds = [
            "ls -R /root/audit-shopee"
        ]
        
        for cmd in cmds:
            print(f"--- Executing: {cmd} ---")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err: print(f"STDERR: {err}")
            
        ssh.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    diagnose()
