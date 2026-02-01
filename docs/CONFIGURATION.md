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
    "pg_trgm"
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

## Multi-Instance Configuration

The tool supports multiple isolated PostgreSQL instances via the `--pg-instance` flag.

### How it works

When you specify an instance name (e.g., `./pgctl --pg-instance myapp setup`):

1.  A build directory is created at `build/myapp/`.
2.  A local configuration file is created at `build/myapp/config/postgres-config.json`.
3.  Init scripts are generated in `build/myapp/init-scripts/`.
4.  The Docker container is named `dev-postgres-myapp` (unless overridden in config).

### Port Management

When running multiple instances simultaneously, you **must** assign unique host ports in their respective configuration files.

1.  Initialize the instance: `./pgctl --pg-instance app2 setup`
2.  Edit `build/app2/config/postgres-config.json`:
    ```json
    {
      "port": 5433,
      "container_name": "dev-postgres-app2"
    }
    ```
3.  Start the instance: `./pgctl --pg-instance app2 start`
