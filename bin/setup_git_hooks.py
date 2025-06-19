#!/usr/bin/env python3
"""
Setup Git Hooks for LisPy

This script configures git to use custom hooks that automatically update
the test count in README.md before each commit.

Usage:
    python bin/setup_git_hooks.py              # Install hooks
    python bin/setup_git_hooks.py --remove     # Remove hooks
    python bin/setup_git_hooks.py --status     # Check hook status
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

def run_git_command(command):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            ['git'] + command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def check_git_repo():
    """Check if we're in a git repository."""
    success, _ = run_git_command(['status'])
    return success

def install_hooks():
    """Install the custom git hooks."""
    print("Installing LisPy git hooks...")
    
    # Make sure we're in a git repo
    if not check_git_repo():
        print("Not in a git repository!")
        return False
    
    # Set git to use our custom hooks directory
    success, output = run_git_command(['config', 'core.hooksPath', '.githooks'])
    
    if not success:
        print(f"Failed to configure git hooks: {output}")
        return False
    
    # Make the hook executable (Unix/Linux/macOS)
    hook_path = PROJECT_ROOT / '.githooks' / 'pre-commit'
    if hook_path.exists() and os.name != 'nt':
        try:
            os.chmod(hook_path, 0o755)
        except OSError as e:
            print(f"Warning: Could not make hook executable: {e}")
    
    print("Git hooks installed successfully!")
    print("The test count in README.md will now be updated automatically before each commit.")
    
    return True

def remove_hooks():
    """Remove the custom git hooks."""
    print("Removing LisPy git hooks...")
    
    # Reset git to use default hooks
    success, output = run_git_command(['config', '--unset', 'core.hooksPath'])
    
    if not success and 'not found' not in output.lower():
        print(f"Failed to remove git hooks: {output}")
        return False
    
    print("Git hooks removed successfully!")
    print("Test count will no longer be updated automatically.")
    
    return True

def check_status():
    """Check the current status of git hooks."""
    print("Git Hooks Status")
    print("=" * 25)
    
    # Check if we're in a git repo
    if not check_git_repo():
        print("Not in a git repository!")
        return False
    
    # Check current hooks path
    success, hooks_path = run_git_command(['config', 'core.hooksPath'])
    
    if success and hooks_path == '.githooks':
        print("Custom hooks are ENABLED")
        print(f"   Hooks directory: {hooks_path}")
        
        # Check if hook files exist
        hook_files = [
            '.githooks/pre-commit',
            '.githooks/pre-commit.bat'
        ]
        
        for hook_file in hook_files:
            hook_path = PROJECT_ROOT / hook_file
            if hook_path.exists():
                print(f"   {hook_file} exists")
            else:
                print(f"   {hook_file} missing")
    else:
        print("Custom hooks are DISABLED")
        print("   Using default git hooks directory")
    
    # Test the update script
    print("\nTesting update script...")
    update_script = PROJECT_ROOT / 'bin' / 'update_test_count.py'
    if update_script.exists():
        try:
            result = subprocess.run([
                sys.executable, str(update_script), '--dry-run'
            ], cwd=PROJECT_ROOT, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("Update script works correctly")
            else:
                print("Update script failed")
                print(f"   Error: {result.stderr}")
        except Exception as e:
            print(f"Could not test update script: {e}")
    else:
        print("Update script not found!")
    
    return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Setup LisPy git hooks")
    
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument('--remove', action='store_true',
                             help='Remove git hooks')
    action_group.add_argument('--status', action='store_true',
                             help='Check git hooks status')
    
    args = parser.parse_args()
    
    print("LisPy Git Hooks Setup")
    print("=" * 30)
    
    if args.remove:
        success = remove_hooks()
    elif args.status:
        success = check_status()
    else:
        success = install_hooks()
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main() 