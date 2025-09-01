#!/usr/bin/env python3
"""
Organize submission files by username after merge.
"""

import json
import yaml
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Any


def load_data_file(filepath: str) -> Dict[str, Any]:
    """Load JSON or YAML file and return data."""
    file_ext = Path(filepath).suffix.lower()
    
    try:
        if file_ext == '.json':
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif file_ext in ['.yaml', '.yml']:
            with open(filepath, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None


def organize_files(source_dir: str, target_dir: str):
    """Organize files from source directory to target directory by username."""
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Create target directory if it doesn't exist
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Track processed files
    processed = 0
    errors = 0
    
    # Process all JSON and YAML files in source directory
    for filepath in source_path.rglob('*'):
        # Skip .gitkeep and example files
        if filepath.name == '.gitkeep':
            continue
        # Skip specific example files that should always be preserved
        if filepath.name in ['example_submission_in.json', 'we_also_accept_submission_in.yaml']:
            print(f"Skipping preserved example file: {filepath}")
            continue
        # Also skip any file with 'example_submission' in the name for backwards compatibility
        if 'example_submission' in filepath.stem.lower():
            print(f"Skipping example file: {filepath}")
            continue
            
        if filepath.suffix.lower() in ['.json', '.yaml', '.yml']:
            print(f"Processing: {filepath}")
            
            # Load data to extract username
            data = load_data_file(str(filepath))
            if not data:
                errors += 1
                continue
            
            # Extract username
            username = data.get('username', '').strip()
            if not username:
                print(f"  ⚠️  No username found in {filepath}")
                errors += 1
                continue
            
            # Sanitize username for directory name
            safe_username = "".join(c for c in username if c.isalnum() or c in '-_')
            if not safe_username:
                print(f"  ⚠️  Invalid username: {username}")
                errors += 1
                continue
            
            # Create user directory
            user_dir = target_path / safe_username
            user_dir.mkdir(exist_ok=True)
            
            # Generate unique filename if needed
            target_file = user_dir / filepath.name
            counter = 1
            while target_file.exists():
                stem = filepath.stem
                suffix = filepath.suffix
                target_file = user_dir / f"{stem}_{counter}{suffix}"
                counter += 1
            
            # Move file
            try:
                shutil.copy2(str(filepath), str(target_file))
                os.remove(str(filepath))
                print(f"  ✅ Moved to: {target_file}")
                processed += 1
            except Exception as e:
                print(f"  ❌ Error moving file: {e}")
                errors += 1
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"  - Files processed: {processed}")
    print(f"  - Errors: {errors}")
    
    # List created user directories
    user_dirs = [d for d in target_path.iterdir() if d.is_dir()]
    if user_dirs:
        print(f"\n📁 User directories created:")
        for user_dir in sorted(user_dirs):
            file_count = len(list(user_dir.glob('*')))
            print(f"  - {user_dir.name}: {file_count} file(s)")
    
    return processed, errors


def main():
    if len(sys.argv) < 3:
        print("Usage: python organize_by_username.py <source_dir> <target_dir>")
        print("Example: python organize_by_username.py submissions/ data/organized/")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    target_dir = sys.argv[2]
    
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist")
        sys.exit(1)
    
    processed, errors = organize_files(source_dir, target_dir)
    
    # Exit with error code if there were any errors
    sys.exit(1 if errors > 0 else 0)


if __name__ == "__main__":
    main()