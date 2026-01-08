# Configuration Guide

## Configuration File

The `config/postgres-config.json` file controls your PostgreSQL setup.

### Options

- **image**: PostgreSQL Docker image (e.g., `postgres:16`, `pgvector/pgvector:pg16`)
- **user**: Database superuser name
- **password**: Database password
- **database**: Default database name
- **port**: Host port to expose PostgreSQL (default: 5432)
- **extensions**: List of PostgreSQL extensions to install
- **custom_types**: SQL statements for custom data types
- **container_name**: Docker container name

### Adding pgvector Support

To enable vector similarity search:
```json
{
  "image": "pgvector/pgvector:pg16",
  "extensions": [
    "vector",
    "pg_trgm",
    ...
  ]
}
```

### Custom Data Types Example
```json
{
  "custom_types": [
    "CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');",
    "CREATE DOMAIN email AS TEXT CHECK (VALUE ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\\\.[A-Z|a-z]{2,}$');"
  ]
}
```

## Init Scripts

SQL scripts in `init-scripts/` are automatically executed when the database is first created:

- `01-extensions.sql` - Auto-generated from config
- `02-custom-types.sql` - Auto-generated from config
- `03-sample-data.sql` - Your custom initialization

You can add more `*.sql` files - they execute in alphabetical order.

## Environment-Specific Configs

For multiple environments:
```bash
cp config/postgres-config.json config/postgres-config.dev.json
cp config/postgres-config.json config/postgres-config.staging.json

# Use different configs
cp config/postgres-config.dev.json config/postgres-config.json
```
