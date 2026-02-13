
import os
import subprocess
import sys
import argparse

def run_command(command):
    """Runs a shell command and returns the output or raises an error."""
    try:
        result = subprocess.run(
            command,
            check=True,
            shell=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        raise e

def main():
    parser = argparse.ArgumentParser(description="Publish changes to GitHub.")
    parser.add_argument("--message", "-m", type=str, required=True, help="Commit message")
    parser.add_argument("--branch", "-b", type=str, default="master", help="Target branch (default: master)")
    
    args = parser.parse_args()
    
    # 1. Check status
    print("--- 1. Checking Git Status ---")
    try:
        status = run_command("git status")
        print(status)
        if "nothing to commit, working tree clean" in status:
            print("\nNothing to commit. Exiting.")
            return
    except Exception:
        print("Not a git repository. Initializing...")
        run_command("git init")
        status = run_command("git status")

    # 2. Add changes
    print("\n--- 2. Adding Changes ---")
    run_command("git add .")
    print("Added all changes.")

    # 3. Commit
    print(f"\n--- 3. Committing with message: '{args.message}' ---")
    run_command(f'git commit -m "{args.message}"')
    print("Committed.")

    # 4. Push
    print(f"\n--- 4. Pushing to origin/{args.branch} ---")
    try:
        run_command(f"git push origin {args.branch}")
        print("\nSUCCESS: Changes pushed to GitHub.")
    except Exception as e:
        print(f"\n[WARNING] Push failed: {e}")
        print("Please ensure remote 'origin' is configured and you are authenticated.")
        print("You may need to run: git remote add origin <url>")

if __name__ == "__main__":
    main()
