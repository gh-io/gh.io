#!/usr/bin/env python3
"""
Simple README update script.
This script checks if the README exists and can be updated.
"""

import os
from datetime import datetime

README_PATH = "profile/README.md"

def update_readme():
    """Update README with current timestamp"""
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(README_PATH), exist_ok=True)
    
    # Read existing README or create default
    if os.path.exists(README_PATH):
        with open(README_PATH, 'r') as f:
            content = f.read()
    else:
        content = "# Profile\n\n"
    
    # Add/update last updated timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add or replace last updated section
    if "Last updated:" in content:
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith("Last updated:"):
                lines[i] = f"Last updated: {timestamp}"
                content = '\n'.join(lines)
                break
    else:
        content += f"\n\nLast updated: {timestamp}\n"
    
    # Write updated README
    with open(README_PATH, 'w') as f:
        f.write(content)
    
    print(f"README updated successfully at {timestamp}")

if __name__ == "__main__":
    update_readme()
