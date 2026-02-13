# Directive: Publish to GitHub

## Goal
To maintain a clean, version-controlled history of the project by pushing validated changes to the remote GitHub repository.

## Inputs
1.  **Commit Message**: A clear, concise description of the changes (e.g., "Add new insight generation script" or "Fix bug in PDF layout").
2.  **Branch**: The target branch, default is `master`.

## Outputs
- Code pushed to `origin/master`.
- Clean `git status`.

## Workflow Steps

### 1. Pre-Publish Check
- **Agent**: You (the AI assistant) or `execution/publish_github.py`.
- **Action**: Check `git status`.
- **Condition**: Ensure you are in the correct root directory.

### 2. Execution
- **Tool**: `execution/publish_github.py`
- **Command**: `python execution/publish_github.py --message "Your commit message"`
- **Details**:
  - The script will automatically:
    1.  Add all changes (`git add .`).
    2.  Commit with the provided message (`git commit -m "..."`).
    3.  Push to remote (`git push origin master`).
  - If any step fails, it will stop and report the error.

### 3. Verification
- **Action**: Verify the output of the script says "Success".
- **Fallback**: If the script fails, manually run the git commands to troubleshoot.

## Quality Constraints
- **Atomic Commits**: Try to group related changes. Don't push broken code if possible.
- **Descriptive Messages**: messages like "fix" or "update" are forbidden. Use "fix: resolve timeout in generation" instead.


import os
import subprocess
import sys
import argparse
from datetime import datetime

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
    status = run_command("git status")
    print(status)
    
    if "nothing to commit, working tree clean" in status:
        print("\nNothing to commit. Exiting.")
        return

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
        print("\nFAILED: Could not push to GitHub. Please check your network or credentials.")
        sys.exit(1)

if __name__ == "__main__":
    main()
