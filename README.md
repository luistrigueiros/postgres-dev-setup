# PostgreSQL Development Environment

Automated PostgreSQL setup for local development with Docker, Python, and UV.

## Features

- 🐘 PostgreSQL 16 with Docker
- 🔧 Configurable extensions (pgvector, full-text search, etc.)
- 📝 Custom data types support
- 🚀 Automated setup and teardown
- 📦 Version-controlled configuration
- 🔄 Easy backup and restore workflows
- 👯 Multi-instance support (run multiple isolated DBs)

## Quick Start
```bash
# 1. Install dependencies (if not already installed)
brew install docker
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Initialize environment
uv run python src/postgres_setup/main.py setup

# 3. Start PostgreSQL
uv run python src/postgres_setup/main.py start

# 4. Connect to database
uv run python src/postgres_setup/main.py psql
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
| `--pg-instance` | Global option to specify instance name (e.g., `--pg-instance analytics`) |

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

## Multi-Instance Support

You can run multiple isolated PostgreSQL instances by using the `--pg-instance` (or `-pgi`) option. Each instance has its own configuration and data.

```bash
# Setup and start a separate instance named 'analytics'
./pgctl --pg-instance analytics setup
./pgctl --pg-instance analytics start

# Check status of the analytics instance
./pgctl -pgi analytics status

# Connect to the analytics instance
./pgctl -pgi analytics psql
```

Instances are stored in the `build/` directory (e.g., `build/analytics/`).

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

# Check status

```bash
./pgctl status
```
The output should look like this:

```bash
📊 PostgreSQL Status (Instance: default, Container: dev-postgres)

NAMES          STATUS                    PORTS
dev-postgres   Up 51 minutes (healthy)   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
```

```bash
./pgctl psql
```

Inside psql, issue test commands, list extensions

```bash

\dx

-- Check version
SELECT version();

-- Exit
\q
```
The output should look like this:

```bash
🔌 Connecting to devdb (Instance: default)...

psql (16.11 (Debian 16.11-1.pgdg13+1))
Type "help" for help.

devdb=# \dx
                                     List of installed extensions
    Name    | Version |   Schema   |                            Description                            
------------+---------+------------+-------------------------------------------------------------------
 btree_gin  | 1.3     | public     | support for indexing common datatypes in GIN
 btree_gist | 1.7     | public     | support for indexing common datatypes in GiST
 pg_trgm    | 1.6     | public     | text similarity measurement and index searching based on trigrams
 pgcrypto   | 1.3     | public     | cryptographic functions
 plpgsql    | 1.0     | pg_catalog | PL/pgSQL procedural language
(5 rows)

```


# Quick Diagnosis
First, let's check if PostgreSQL is actually accessible:

## Test 1: Check if port is listening
```bash
lsof -i :5432
```

## Test 2: Try connecting with psql from your Mac (not Docker)

Install postgresql client if needed: 
```bash
brew install postgresql
psql -h localhost -p 5432 -U devuser -d devdb
```

## Test 3: Test with netcat
```bash
nc -zv localhost 5432
```


## License

MIT - Use freely for your projects
