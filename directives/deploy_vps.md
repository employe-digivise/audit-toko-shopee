# Deploy to VPS (Port 1101)

This directive outlines the steps to deploy the Audit Report Server to a VPS on Port 1101 using the automated Python script.

## Goal
Host the generated HTML audit reports on a VPS so they are accessible via `http://<vps-ip>:1101`.

## Prerequisites
- **Credentials**: Ensure `.env` contains:
  - `SSH_ROOT=ssh user@ip`
  - `VPS_PASSWORD=yourpassword`
- **Port 1101**: Must be open in the VPS firewall.

## Deployment Method (Automated)

We use a Python script `execution/deploy_to_vps.py` that handles zipping, uploading (SFTP), and remote execution (venv creation, dependency install, server start).

1. **Prepare Environment**:
   Ensure local dependencies are installed:
   ```bash
   pip install paramiko python-dotenv
   ```

2. **Run Deployment Script**:
   ```bash
   python execution/deploy_to_vps.py
   ```

3. **What the Script Does**:
   - Creates a zip of the project (handling Windows/Linux path differences).
   - Uploads zip to `/root/audit-shopee/app_deploy.zip`.
   - Remotely unzips the file.
   - Sets up a Python Virtual Environment (`venv`) on the VPS.
   - Installs `flask` and `jinja2` inside the venv.
   - Kills any existing `serve_report.py` process.
   - Starts the server with `nohup` on port 1101.

4. **Verification (Deployment)**:
   The script will output the verification URL, e.g., `http://31.97.222.83:1101`.

## Manual Fallback (If Script Fails)
If the script fails, you can try manual deployment:
1. Copy files to VPS: `scp -r . root@<ip>:/root/audit-shopee`
2. SSH into VPS.
3. Run:
   ```bash
   cd /root/audit-shopee
   python3 -m venv venv
   ./venv/bin/pip install flask jinja2
   nohup ./venv/bin/python execution/serve_report.py &
   ```
