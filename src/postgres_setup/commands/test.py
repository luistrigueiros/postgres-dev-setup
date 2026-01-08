"""Test command - Test PostgreSQL connectivity."""

from .base import BaseCommand


class TestCommand(BaseCommand):
    """Test PostgreSQL connection from host."""

    name = "test"
    description = "Test database connectivity"

    def execute(self) -> None:
        """Test PostgreSQL connection from host."""
        print("🔍 Testing PostgreSQL connection...\n")
        config = self.config_manager.load()

        # Test 1: Container health
        print("1. Container health check:")
        success, _ = self.docker.exec_command(
            config['container_name'],
            ["pg_isready", "-U", config['user']]
        )
        print(f"   {'✓' if success else '✗'} Container internal connection")

        # Test 2: Port listening
        print("\n2. Port availability:")
        success, output = self.docker.run_command([
            "lsof", "-i", f":{config['port']}"
        ])
        if success and output:
            print(f"   ✓ Port {config['port']} is listening")
        else:
            print(f"   ✗ Port {config['port']} not accessible")

        # Test 3: Network connectivity
        print("\n3. Network connectivity:")
        success, _ = self.docker.run_command([
            "nc", "-zv", "localhost", str(config['port'])
        ])
        print(f"   {'✓' if success else '✗'} Network connection")

        # Test 4: Docker network
        print("\n4. Docker network info:")
        container_ip = self.docker.get_container_ip(config['container_name'])
        if container_ip:
            print(f"   Container IP: {container_ip}")

        # Test 5: Actual psql connection
        print("\n5. Testing psql connection:")
        success, _ = self.docker.exec_command(
            config['container_name'],
            [
                "psql", "-U", config['user'], "-d", config['database'],
                "-c", "SELECT version();"
            ]
        )
        print(f"   {'✓ Connected successfully' if success else '✗ Connection failed'}")

        if not success:
            print("\n⚠️  Troubleshooting steps:")
            print("   1. Restart Docker Desktop")
            print("   2. Run: ./pgctl restart")
            print("   3. Check firewall settings")
            print("   4. Try: telnet localhost 5432")