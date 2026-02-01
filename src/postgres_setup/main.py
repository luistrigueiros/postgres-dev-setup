#!/usr/bin/env python3
"""
PostgreSQL Development Environment Setup
Requires: uv, docker
Usage: pgctl [command]
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from postgres_setup.commands import app  # noqa: E402


def main():
    app(prog_name="pgctl")

if __name__ == "__main__":
    main()
