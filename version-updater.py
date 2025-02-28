import sys
import os
from datetime import datetime

VERSION_FILE = 'version'
VERSION_LOG_FILE = 'version_log'

def read_version():
    if not os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'w') as f:
            f.write('1.0.0')
        return '1.0.0'
    
    with open(VERSION_FILE, 'r') as f:
        version = f.readline().strip()
        if not version:
            version = '1.0.0'
            with open(VERSION_FILE, 'w') as fw:
                fw.write(version)
        return version

def write_version(version):
    with open(VERSION_FILE, 'w') as f:
        f.write(version)

def log_version_update(old_version, new_version, update_type):
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]
    log_entry = f'[{new_version}] <- [{old_version}] [{timestamp}] {update_type} update\n'
    
    with open(VERSION_LOG_FILE, 'a') as f:
        f.write(log_entry)

def increment_version(version, update_type):
    parts = list(map(int, version.split('.')))
    
    if update_type == 'major':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif update_type == 'minor':
        parts[1] += 1
        parts[2] = 0
    elif update_type == 'patch':
        parts[2] += 1
    else:
        raise ValueError(f"Invalid update type: {update_type}")
    
    return '.'.join(map(str, parts))

def main():
    if len(sys.argv) != 2:
        print("Usage: python version_updater.py <major|minor|patch>")
        return
    
    update_type = sys.argv[1]
    if update_type not in ['major', 'minor', 'patch']:
        print("Исользуй 'major', 'minor', 'patch'.")
        return
    
    old_version = read_version()
    new_version = increment_version(old_version, update_type)
    
    write_version(new_version)
    log_version_update(old_version, new_version, update_type)
    
    print(f"Version updated from {old_version} to {new_version} ({update_type} update)")

if __name__ == "__main__":
    main()