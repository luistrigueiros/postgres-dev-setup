# PostgreSQL Development Environment

Automated PostgreSQL setup for local development with Docker, Python, and UV.

## Features

- 🐘 PostgreSQL 16 with Docker
- 🔧 Configurable extensions (pgvector, full-text search, etc.)
- 📝 Custom data types support
- 🚀 Automated setup and teardown
- 📦 Version-controlled configuration
- 🔄 Easy backup and restore workflows

## Quick Start
```bash
# 1. Install dependencies (if not already installed)
brew install docker
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Initialize environment
uv run python src/postgres_setup/setup.py setup

# 3. Start PostgreSQL
uv run python src/postgres_setup/setup.py start

# 4. Connect to database
uv run python src/postgres_setup/setup.py psql
```

Or use the convenience wrapper:
```bash
./pgctl setup
./pgctl start
./pgctl psql
```

## Commands

| Command | Description |
|---------|-------------|
| `setup` | Initialize configuration and generate scripts |
| `start` | Start PostgreSQL container |
| `stop` | Stop container (preserves data) |
| `restart` | Restart container |
| `destroy` | Stop and remove all data ⚠️ |
| `logs` | View PostgreSQL logs |
| `psql` | Connect with psql client |
| `status` | Show container status |
| `info` | Display connection information |

## Configuration

Edit `config/postgres-config.json` to customize:

- PostgreSQL version
- Database credentials
- Installed extensions
- Custom data types
- Port mapping

See [Configuration Guide](docs/CONFIGURATION.md) for details.

## Common Workflows

### Daily Development
```bash
./pgctl start    # Start database
./pgctl psql     # Connect and work
./pgctl stop     # Stop when done
```

### Adding Extensions

1. Edit `config/postgres-config.json`:
```json
   {
     "extensions": ["vector", "pg_trgm", "pgcrypto"]
   }
```

2. Regenerate and restart:
```bash
   ./pgctl setup
   ./pgctl restart
```

### Fresh Database
```bash
./pgctl destroy  # Removes all data
./pgctl setup
./pgctl start
```

### Checking Status
```bash
./pgctl status   # Container status
./pgctl info     # Connection details
./pgctl logs     # View logs
```

## Project Structure

.
├── config/
│   └── postgres-config.json    # Main configuration
├── src/
│   └── postgres_setup/
│       ├── init.py
│       └── setup.py            # Main script
├── init-scripts/               # Generated SQL (gitignored)
├── docs/
│   └── CONFIGURATION.md        # Detailed config docs
├── docker-compose.yml          # Generated Docker config
├── pgctl                       # Convenience wrapper
└── README.md

## Connection Details

After starting, connect with your favorite tool:

**psql (via Docker)**:
```bash
./pgctl psql
```

**External tool** (DBeaver, DataGrip, etc.):
- Host: `localhost`
- Port: `5432`
- Database: `devdb`
- User: `devuser`
- Password: `devpass`

**Connection URI**:
postgresql://devuser:devpass@localhost:5432/devdb

## Troubleshooting

### Port already in use

Change port in `config/postgres-config.json`:
```json
{
  "port": 5433
}
```

Then run:
```bash
./pgctl setup
./pgctl restart
```

### Container won't start
```bash
./pgctl logs     # Check logs
docker ps -a     # Check container status
```

### Fresh start
```bash
./pgctl destroy
./pgctl setup
./pgctl start
```

### Test the Setup
Step 9: Test the Setup
bash# Run the setup
uv run python src/postgres_setup/setup.py setup

# Start PostgreSQL
uv run python src/postgres_setup/setup.py start

# Check status
uv run python src/postgres_setup/setup.py status

# Connect to database
uv run python src/postgres_setup/setup.py psql
Inside psql, test:
sql-- List extensions
\dx

-- Check version
SELECT version();

-- Exit
\q

### Quick Diagnosis
First, let's check if PostgreSQL is actually accessible:
bash# Test 1: Check if port is listening
lsof -i :5432

# Test 2: Try connecting with psql from your Mac (not Docker)
# Install postgresql client if needed: brew install postgresql
psql -h localhost -p 5432 -U devuser -d devdb

# Test 3: Test with netcat
nc -zv localhost 5432

## Contributing

This is a template - customize it for your needs! Common customizations:

- Add migration tools (Alembic, Flyway)
- Include backup/restore scripts
- Add monitoring (pgAdmin, pg_stat_statements)
- Configure replication for testing


## License

MIT - Use freely for your projects
