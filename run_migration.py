#!/usr/bin/env python3
"""
Script to run database migrations using Alembic
"""

import os
import sys
import subprocess

def run_alembic_command(command):
    """Run Alembic command with uv"""
    try:
        result = subprocess.run(['uv', 'run', 'alembic'] + command,
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running alembic {command}:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    print("Running database migrations...")

    # Check if DATABASE_URL is set
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("DATABASE_URL environment variable not set")
        print("Using default MariaDB URL from alembic.ini")

    # Run the migration
    success = run_alembic_command(['upgrade', 'head'])

    if success:
        print("✅ Database migration completed successfully!")
    else:
        print("❌ Database migration failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()