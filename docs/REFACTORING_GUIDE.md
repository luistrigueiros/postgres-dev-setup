# Refactoring Guide: Modular Command Structure

This guide shows you how to migrate from the monolithic `setup.py` to a modular, extensible command structure.

## Why Refactor?

**Before**: One 300+ line file with all commands  
**After**: 10+ focused files, each with a single responsibility  

**Benefits:**
- ✅ Easy to add new commands (just create a new file)
- ✅ Better code organization and maintainability
- ✅ Automatic command discovery
- ✅ Easier testing (test each command independently)
- ✅ Better separation of concerns

## New Project Structure

```
src/postgres_setup/
├── __init__.py              # Package marker
├── cli.py                   # Main entry point (40 lines)
├── config.py                # Configuration management (60 lines)
├── docker_manager.py        # Docker operations (150 lines)
└── commands/
    ├── __init__.py          # Command discovery (40 lines)
    ├── base.py              # Base command class (50 lines)
    ├── setup.py             # Setup command (50 lines)
    ├── start.py             # Start command (70 lines)
    ├── stop.py              # Stop command (20 lines)
    ├── restart.py           # Restart command (20 lines)
    ├── destroy.py           # Destroy command (30 lines)
    ├── logs.py              # Logs command (20 lines)
    ├── psql.py              # Psql command (20 lines)
    ├── status.py            # Status command (20 lines)
    ├── info.py              # Info command (30 lines)
    └── test.py              # Test command (60 lines)
```

## Step-by-Step Migration

### Step 1: Backup Current Setup

```bash
# Backup your current working setup
cp src/postgres_setup/setup.py src/postgres_setup/setup.py.backup

# Commit current state
git add -A
git commit -m "Backup before refactoring"
```

### Step 2: Create New Directory Structure

```bash
# Create commands directory
mkdir -p src/postgres_setup/commands

# Create __init__.py files
touch src/postgres_setup/commands/__init__.py
```

### Step 3: Add Core Files

Create these files in order (copy from artifacts above):

1. **src/postgres_setup/config.py** - Configuration management
2. **src/postgres_setup/docker_manager.py** - Docker operations
3. **src/postgres_setup/commands/base.py** - Base command class
4. **src/postgres_setup/commands/__init__.py** - Command discovery

```bash
# Add to git
git add src/postgres_setup/config.py
git add src/postgres_setup/docker_manager.py
git add src/postgres_setup/commands/base.py
git add src/postgres_setup/commands/__init__.py
git commit -m "Add core refactored modules"
```

### Step 4: Add Command Files

Create command files (copy from artifacts above):

```bash
# Create all command files
touch src/postgres_setup/commands/setup.py
touch src/postgres_setup/commands/start.py
touch src/postgres_setup/commands/stop.py
touch src/postgres_setup/commands/status.py
touch src/postgres_setup/commands/test.py
# ... and so on

# Add to git
git add src/postgres_setup/commands/
git commit -m "Add modular command files"
```

### Step 5: Create New CLI Entry Point

```bash
# Create new cli.py
# Copy content from cli.py artifact above

git add src/postgres_setup/cli.py
git commit -m "Add new CLI entry point"
```

### Step 6: Update pgctl Wrapper

```bash
# Update pgctl to use new CLI
cat > pgctl << 'EOF'
#!/bin/bash
# Convenience wrapper for postgres setup
uv run python src/postgres_setup/cli.py "$@"
EOF

chmod +x pgctl

git add pgctl
git commit -m "Update pgctl to use new CLI"
```

### Step 7: Test New Structure

```bash
# Test that everything works
./pgctl setup
./pgctl status
./pgctl start
./pgctl test
./pgctl stop
```

### Step 8: Remove Old File (Optional)

```bash
# Once everything works, remove old setup.py
git rm src/postgres_setup/setup.py

# Or keep as backup
git mv src/postgres_setup/setup.py src/postgres_setup/setup.py.old

git commit -m "Remove old monolithic setup.py"
```

## Adding New Commands

Now adding a command is as simple as creating a new file!

### Example: Add "backup" Command

Create `src/postgres_setup/commands/backup.py`:

```python
"""Backup command - Backup PostgreSQL database."""

from datetime import datetime
from pathlib import Path
from .base import BaseCommand


class BackupCommand(BaseCommand):
    """Backup PostgreSQL database."""
    
    name = "backup"
    description = "Create database backup"
    
    def execute(self) -> None:
        """Create database backup."""
        print("💾 Creating backup...")
        
        config = self.config_manager.load()
        
        # Create backup directory
        backup_dir = self.project_root / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"backup_{timestamp}.sql"
        
        # Run pg_dump
        success, output = self.docker.exec_command(
            config['container_name'],
            [
                "pg_dump",
                "-U", config['user'],
                "-d", config['database'],
                "-f", f"/tmp/backup_{timestamp}.sql"
            ]
        )
        
        if success:
            # Copy from container to host
            self.docker.run_command([
                "docker", "cp",
                f"{config['container_name']}:/tmp/backup_{timestamp}.sql",
                str(backup_file)
            ])
            self.print_success(f"Backup saved to {backup_file}")
        else:
            self.print_error(f"Backup failed: {output}")
```

**That's it!** The command is automatically discovered and available:

```bash
./pgctl backup  # Works immediately!
```

### Example: Add "restore" Command

Create `src/postgres_setup/commands/restore.py`:

```python
"""Restore command - Restore PostgreSQL database from backup."""

import sys
from pathlib import Path
from .base import BaseCommand


class RestoreCommand(BaseCommand):
    """Restore PostgreSQL database from backup."""
    
    name = "restore"
    description = "Restore database from backup"
    
    def execute(self) -> None:
        """Restore database from backup."""
        if len(sys.argv) < 3:
            self.print_error("Usage: ./pgctl restore <backup_file>")
            sys.exit(1)
        
        backup_file = Path(sys.argv[2])
        
        if not backup_file.exists():
            self.print_error(f"Backup file not found: {backup_file}")
            sys.exit(1)
        
        print(f"📥 Restoring from {backup_file}...")
        
        config = self.config_manager.load()
        
        # Copy backup to container
        success, _ = self.docker.run_command([
            "docker", "cp",
            str(backup_file),
            f"{config['container_name']}:/tmp/restore.sql"
        ])
        
        if not success:
            self.print_error("Failed to copy backup to container")
            sys.exit(1)
        
        # Restore using psql
        success, output = self.docker.exec_command(
            config['container_name'],
            [
                "psql",
                "-U", config['user'],
                "-d", config['database'],
                "-f", "/tmp/restore.sql"
            ]
        )
        
        if success:
            self.print_success("Restore completed successfully")
        else:
            self.print_error(f"Restore failed: {output}")
```

## Complete File Templates

### Minimal Command Template

```python
"""[Command Name] - [Brief description]."""

from .base import BaseCommand


class [Name]Command(BaseCommand):
    """[Detailed description]."""
    
    name = "[command-name]"
    description = "[Short description for help]"
    
    def execute(self) -> None:
        """Execute the command."""
        # Your code here
        pass
```

### Command with Arguments Template

```python
"""[Command Name] - [Brief description]."""

import sys
from .base import BaseCommand


class [Name]Command(BaseCommand):
    """[Detailed description]."""
    
    name = "[command-name]"
    description = "[Short description]"
    
    def execute(self) -> None:
        """Execute the command."""
        # Parse arguments
        if len(sys.argv) < 3:
            self.print_error("Usage: ./pgctl [command] <arg>")
            sys.exit(1)
        
        arg = sys.argv[2]
        
        # Your code here
        config = self.config_manager.load()
        success, output = self.docker.run_command(["docker", "ps"])
        
        if success:
            self.print_success("Operation successful")
        else:
            self.print_error(f"Operation failed: {output}")
```

## Benefits in Practice

### Before (Monolithic)
To add a command:
1. Edit 300+ line file
2. Find the right place to add code
3. Add to commands dict
4. Risk breaking existing commands
5. Hard to test in isolation

### After (Modular)
To add a command:
1. Create new 20-40 line file
2. Inherit from `BaseCommand`
3. Set `name` and `description`
4. Implement `execute()`
5. Done! Auto-discovered

### Testing Benefits

```bash
# Test individual command
python -m pytest tests/test_backup_command.py

# Test just Docker operations
python -m pytest tests/test_docker_manager.py

# Test configuration
python -m pytest tests/test_config.py
```

## Remaining Commands to Implement

Create these files to complete the refactoring:

- `commands/restart.py` - Restart container
- `commands/destroy.py` - Destroy with confirmation
- `commands/logs.py` - Show logs
- `commands/psql.py` - Connect with psql
- `commands/info.py` - Show connection info

Use the templates above - each should be 20-40 lines!

## Troubleshooting

### Commands not discovered?

Check that:
1. File is in `src/postgres_setup/commands/`
2. Class inherits from `BaseCommand`
3. Class has `name` and `description` attributes
4. Class implements `execute()` method

### Import errors?

```bash
# Verify package structure
tree src/postgres_setup/

# Should see:
# src/postgres_setup/
# ├── __init__.py
# ├── cli.py
# ├── config.py
# ├── docker_manager.py
# └── commands/
#     ├── __init__.py
#     ├── base.py
#     └── [command files]
```

## Next Steps

1. **Add more commands**: backup, restore, migrate, seed
2. **Add tests**: pytest for each command
3. **Add logging**: Python logging module
4. **Add config validation**: pydantic for config
5. **Add shell completion**: argcomplete

## Questions?

The beauty of this structure is that each file is small and focused. If you need to understand or modify a command, you only need to look at one ~30 line file instead of scrolling through 300+ lines!

Happy coding! 🚀