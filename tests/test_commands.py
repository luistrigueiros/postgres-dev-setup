import pytest
from unittest.mock import MagicMock, patch, mock_open
from argparse import Namespace
from pathlib import Path

from postgres_setup.commands.status import StatusCommand
from postgres_setup.commands.start import StartCommand
from postgres_setup.commands.stop import StopCommand
from postgres_setup.commands.restart import RestartCommand
from postgres_setup.commands.destroy import DestroyCommand
from postgres_setup.commands.info import InfoCommand
from postgres_setup.commands.logs import LogsCommand
from postgres_setup.commands.psql import PsqlCommand
from postgres_setup.commands.setup import SetupCommand

@pytest.fixture
def mock_run_command():
    with patch("postgres_setup.commands.Command.run_command") as mock:
        mock.return_value = (True, "mock output")
        yield mock

@pytest.fixture
def mock_config_exists():
    with patch("pathlib.Path.exists") as mock:
        mock.return_value = True
        yield mock

@pytest.fixture
def mock_config_load():
    with patch("builtins.open", mock_open(read_data='{"port": 5432, "database": "devdb", "user": "devuser", "password": "devpass", "container_name": "dev-postgres", "extensions": ["pg_trgm"]}')):
        yield

def test_status_command(mock_run_command):
    cmd = StatusCommand()
    cmd.run(Namespace())
    mock_run_command.assert_called_once()
    assert "docker" in mock_run_command.call_args[0][0]

def test_stop_command(mock_run_command):
    cmd = StopCommand()
    cmd.run(Namespace())
    mock_run_command.assert_called_with(["docker-compose", "down"])

def test_start_command(mock_run_command, mock_config_load, mock_config_exists):
    with patch("time.sleep", return_value=None):
        cmd = StartCommand()
        # Mock pg_isready to succeed on first try, then show_extensions
        mock_run_command.side_effect = [(True, ""), (True, ""), (True, "")]
        cmd.run(Namespace())
        assert mock_run_command.call_count >= 3
        assert mock_run_command.call_args_list[0][0][0] == ["docker-compose", "up", "-d"]

def test_restart_command(mock_run_command, mock_config_load, mock_config_exists):
    with patch("time.sleep", return_value=None):
        cmd = RestartCommand()
        # Mock down, up, pg_isready, and show_extensions
        mock_run_command.side_effect = [(True, ""), (True, ""), (True, ""), (True, "")]
        cmd.run(Namespace())
        assert mock_run_command.call_count >= 4
        assert mock_run_command.call_args_list[0][0][0] == ["docker-compose", "down"]
        assert mock_run_command.call_args_list[1][0][0] == ["docker-compose", "up", "-d"]

def test_destroy_command_confirmed(mock_run_command):
    with patch("builtins.input", return_value="yes"):
        cmd = DestroyCommand()
        cmd.run(Namespace())
        mock_run_command.assert_called_with(["docker-compose", "down", "-v"])

def test_destroy_command_aborted(mock_run_command):
    with patch("builtins.input", return_value="no"):
        cmd = DestroyCommand()
        cmd.run(Namespace())
        mock_run_command.assert_not_called()

def test_info_command(mock_config_load, mock_config_exists):
    cmd = InfoCommand()
    with patch("builtins.print") as mock_print:
        cmd.run(Namespace())
        # Check if some expected info was printed
        printed_text = "".join(call.args[0] for call in mock_print.call_args_list if call.args)
        assert "5432" in printed_text
        assert "devdb" in printed_text

def test_logs_command(mock_run_command):
    cmd = LogsCommand()
    cmd.run(Namespace())
    mock_run_command.assert_called_with(["docker-compose", "logs", "-f", "postgres"], capture_output=False)

def test_psql_command(mock_run_command, mock_config_load, mock_config_exists):
    cmd = PsqlCommand()
    cmd.run(Namespace())
    assert "psql" in mock_run_command.call_args[0][0]
    assert mock_run_command.call_args[1]["capture_output"] is False

def test_setup_command(mock_config_exists):
    config_data = '{"image": "postgres:16", "port": 5432, "database": "devdb", "user": "devuser", "password": "devpass", "container_name": "dev-postgres", "extensions": ["pg_trgm"], "custom_types": []}'
    with patch("pathlib.Path.mkdir"), \
         patch("pathlib.Path.write_text"), \
         patch("builtins.open", mock_open(read_data=config_data)):
        cmd = SetupCommand()
        cmd.run(Namespace())
        # Verification of file writes could be more detailed, but this checks it runs
