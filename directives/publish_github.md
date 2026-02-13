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
