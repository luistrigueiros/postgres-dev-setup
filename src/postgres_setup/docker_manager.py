"""Docker operations management."""

import subprocess
import time
from pathlib import Path
from typing import Tuple, Dict, Any


class DockerManager:
    """Manages Docker operations for PostgreSQL."""

    def __init__(self, project_root: Path):
        self.project_root = project_root

    def run_command(
            self,
            cmd: list[str],
            capture_output: bool = True
    ) -> Tuple[bool, str]:
        """Execute shell command and return success status and output."""
        try:
            if capture_output:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    cwd=self.project_root
                )
                return True, result.stdout
            else:
                subprocess.run(cmd, check=True, cwd=self.project_root)
                return True, ""
        except subprocess.CalledProcessError as e:
            return False, e.stderr if capture_output else str(e)

    def compose_up(self) -> Tuple[bool, str]:
        """Start containers with docker-compose."""
        return self.run_command(["docker-compose", "up", "-d"])

    def compose_down(self, remove_volumes: bool = False) -> Tuple[bool, str]:
        """Stop containers with docker-compose."""
        cmd = ["docker-compose", "down"]
        if remove_volumes:
            cmd.append("-v")
        return self.run_command(cmd)

    def compose_logs(self, service: str = "postgres") -> None:
        """Show logs for a service."""
        self.run_command(
            ["docker-compose", "logs", "-f", service],
            capture_output=False
        )

    def exec_command(
            self,
            container: str,
            cmd: list[str],
            interactive: bool = False
    ) -> Tuple[bool, str]:
        """Execute command in container."""
        docker_cmd = ["docker", "exec"]
        if interactive:
            docker_cmd.append("-it")
        docker_cmd.append(container)
        docker_cmd.extend(cmd)

        return self.run_command(docker_cmd, capture_output=not interactive)

    def wait_for_healthy(
            self,
            container: str,
            user: str,
            timeout: int = 30
    ) -> bool:
        """Wait for PostgreSQL to be healthy."""
        for i in range(timeout):
            time.sleep(1)
            success, _ = self.exec_command(
                container,
                ["pg_isready", "-U", user]
            )
            if success:
                return True
            print(".", end="", flush=True)
        return False

    def get_container_status(self, container: str) -> Tuple[bool, str]:
        """Get status of a container."""
        return self.run_command([
            "docker", "ps", "-a",
            "--filter", f"name={container}",
            "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ])

    def get_container_ip(self, container: str) -> str:
        """Get IP address of container."""
        success, output = self.run_command([
            "docker", "inspect", "-f",
            "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}",
            container
        ])
        return output.strip() if success else ""

    def generate_compose_file(
            self,
            compose_file: Path,
            config: Dict[str, Any]
    ) -> None:
        """Generate docker-compose.yml from config."""
        compose_content = f"""version: '3.8'

services:
  postgres:
    image: {config['image']}
    container_name: {config['container_name']}
    environment:
      POSTGRES_USER: {config['user']}
      POSTGRES_PASSWORD: {config['password']}
      POSTGRES_DB: {config['database']}
      POSTGRES_INITDB_ARGS: "-E UTF8 --locale=en_US.UTF-8"
    ports:
      - "127.0.0.1:{config['port']}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {config['user']}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - postgres_network

volumes:
  postgres_data:
    driver: local

networks:
  postgres_network:
    driver: bridge
"""
        compose_file.write_text(compose_content)

    def generate_init_scripts(
            self,
            init_dir: Path,
            config: Dict[str, Any]
    ) -> None:
        """Generate initialization SQL scripts."""
        init_dir.mkdir(exist_ok=True)

        # Extensions script
        extensions_sql = """-- Install PostgreSQL extensions
-- This script runs automatically when the database is first created

"""
        for ext in config['extensions']:
            extensions_sql += f"CREATE EXTENSION IF NOT EXISTS {ext};\n"

        extensions_sql += """
                          -- Verify extensions
                          SELECT extname, extversion \
                          FROM pg_extension \
                          ORDER BY extname; \
                          """

        (init_dir / "01-extensions.sql").write_text(extensions_sql)

        # Custom types script
        if config['custom_types']:
            types_sql = """-- Custom data types
-- Define your custom PostgreSQL types here

"""
            for custom_type in config['custom_types']:
                types_sql += f"{custom_type}\n\n"

            (init_dir / "02-custom-types.sql").write_text(types_sql)

        # Sample data script
        sample_sql = """-- Sample initialization script
-- You can add your own tables and seed data here

-- Example: Create a sample table
-- CREATE TABLE IF NOT EXISTS users (
--     id SERIAL PRIMARY KEY,
--     email TEXT NOT NULL UNIQUE,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );
"""
        (init_dir / "03-sample-data.sql").write_text(sample_sql)