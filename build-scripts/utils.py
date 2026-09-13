"""Build utilities"""

import os
import subprocess
import sys


def run_command(cmd, cwd=None, check=True):
    """Run a command and handle errors"""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, cwd=cwd, check=check)
    except subprocess.CalledProcessError:
        return False
    return result.returncode == 0


def check_file_exists(path, description):
    """Check if a file exists"""
    if not os.path.exists(path):
        print(f"ERROR: {description} not found at {path}")
        return False
    print(f"✓ {description} found")
    return True


def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 9):
        print(f"ERROR: Python 3.9+ required, got {sys.version}")
        return False
    print(f"✓ Python version OK: {sys.version}")
    return True
