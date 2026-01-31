import pytest
import subprocess
import os
import tempfile
import yaml
import json
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
from typing import Dict, List, Any, Optional
import docker
import time

# Skip Docker tests if Docker is not available
try:
    client = docker.from_env()
    client.ping()
    DOCKER_AVAILABLE = True
except:
    DOCKER_AVAILABLE = False

pytestmark = pytest.mark.skipif(
    not DOCKER_AVAILABLE,
    reason="Docker is not available or not running"
)

class TestDeployScript:
    """Unit tests for the deployment script functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.deploy_commands = [
            "cd /path/to/synova",
            "docker-compose -f docker-compose.prod.yml pull",
            "docker-compose -f docker-compose.prod.yml up -d --no-deps web",
            "docker system prune -f"
        ]
    
    @patch('subprocess.run')
    def test_deploy_script_commands_execution(self, mock_run):
        """Test that all deploy commands are executed in sequence with correct parameters."""
        # Mock successful command execution
        mock_run.return_value = Mock(returncode=0, stdout="Success", stderr="")
        
        # Execute deploy script commands
        for command in self.deploy_commands:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            assert result.returncode == 0
        
        # Verify all commands were called
        assert mock_run.call_count == len(self.deploy_commands)
        
        # Verify the commands were called with correct arguments and order
        expected_calls = [
            call(self.deploy_commands[0], shell=True, capture_output=True, text=True, check=True),
            call(self.deploy_commands[1], shell=True, capture_output=True, text=True, check=True),
            call(self.deploy_commands[2], shell=True, capture_output=True, text=True, check=True),
            call(self.deploy_commands[3], shell=True, capture_output=True, text=True, check=True)
        ]
        mock_run.assert_has_calls(expected_calls, any_order=False)
    
    @pytest.mark.parametrize("failed_command_index, expected_error", [
        (0, "Failed to change directory"),
        (1, "Failed to pull Docker images"),
        (2, "Failed to start containers"),
        (3, "Failed to prune Docker system")
    ])
    @patch('subprocess.run')
    def test_deploy_script_failure_handling(self, mock_run, failed_command_index, expected_error):
        """Test that deployment failures are properly handled for each command."""
        # Mock successful execution for commands before the failing one
        def mock_run_side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get('args', '')
            cmd_index = self.deploy_commands.index(cmd) if cmd in self.deploy_commands else -1
            
            if cmd_index == failed_command_index:
                raise subprocess.CalledProcessError(
                    returncode=1,
                    cmd=cmd,
                    output=f"{expected_error} output",
                    stderr=f"{expected_error} error"
                )
            return Mock(returncode=0, stdout="Success", stderr="")

        mock_run.side_effect = mock_run_side_effect
        
        # Test that the correct exception is raised
        with pytest.raises(subprocess.CalledProcessError) as exc_info:
            for command in self.deploy_commands:
                subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    check=True
                )
        
        # Verify the error message contains the expected error
        assert expected_error.lower() in str(exc_info.value).lower()
        
        # Verify no further commands were executed after the failure
        assert mock_run.call_count == failed_command_index + 1
    
    @patch('subprocess.run')
    def test_docker_compose_pull_command(self, mock_run):
        """Test the docker-compose pull command specifically."""
        mock_run.return_value = Mock(returncode=0, stdout="Pulled successfully", stderr="")
        
        command = "docker-compose -f docker-compose.prod.yml pull"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        
        mock_run.assert_called_once_with(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        assert result.returncode == 0
    
    @patch('subprocess.run')
    def test_docker_compose_up_command(self, mock_run):
        """Test the docker-compose up command with specific flags."""
        mock_run.return_value = Mock(returncode=0, stdout="Container started", stderr="")
        
        command = "docker-compose -f docker-compose.prod.yml up -d --no-deps web"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        
        mock_run.assert_called_once_with(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        assert result.returncode == 0
    
    @patch('subprocess.run')
    def test_docker_prune_command(self, mock_run):
        """Test the docker system prune command."""
        mock_run.return_value = Mock(returncode=0, stdout="Pruned", stderr="")
        
        command = "docker system prune -f"
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        
        mock_run.assert_called_once_with(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        assert result.returncode == 0
    
    def test_deploy_script_structure(self):
        """Test that the deploy script contains all expected commands."""
        expected_commands = [
            "cd /path/to/synova",
            "docker-compose -f docker-compose.prod.yml pull",
            "docker-compose -f docker-compose.prod.yml up -d --no-deps web",
            "docker system prune -f"
        ]
        
        assert self.deploy_commands == expected_commands
        assert len(self.deploy_commands) == 4
    
    @patch('os.chdir')
    @patch('subprocess.run')
    def test_directory_change_before_docker_commands(self, mock_run, mock_chdir):
        """Test that directory change happens before Docker commands."""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")
        
        # Simulate the script execution
        os.chdir("/path/to/synova")
        
        docker_commands = [
            "docker-compose -f docker-compose.prod.yml pull",
            "docker-compose -f docker-compose.prod.yml up -d --no-deps web",
            "docker system prune -f"
        ]
        
        for command in docker_commands:
            subprocess.run(command, shell=True, check=True)
        
        # Verify directory was changed
        mock_chdir.assert_called_once_with("/path/to/synova")
        
        # Verify Docker commands were executed
        assert mock_run.call_count == 3


class TestDeployScriptIntegration:
    """Integration tests for deploy script functionality."""
    
    @pytest.fixture
    def deploy_file_path(self) -> Path:
        """Return the path to the deploy.yml file."""
        return Path(__file__).parent.parent / '.github' / 'workflows' / 'deploy.yml'
    
    @pytest.fixture
    def deploy_config(self, deploy_file_path: Path) -> Dict[str, Any]:
        """Load and return the deploy.yml content as a dictionary."""
        with open(deploy_file_path, 'r') as f:
            return yaml.safe_load(f)
    
    def test_deploy_script_file_exists(self, deploy_file_path: Path):
        """Test that the deploy.yml file exists and contains the script."""
        assert deploy_file_path.exists(), "deploy.yml file should exist"
        
        content = deploy_file_path.read_text()
        
        # Check that the script section exists with all required commands
        required_commands = [
            'script: |',
            'cd /path/to/synova',
            'docker-compose -f docker-compose.prod.yml pull',
            'docker-compose -f docker-compose.prod.yml up -d --no-deps web',
            'docker system prune -f'
        ]
        
        for cmd in required_commands:
            assert cmd in content, f"Required command not found: {cmd}"
    
    def test_deploy_workflow_structure(self, deploy_config: Dict[str, Any]):
        """Test that the deploy workflow has the correct structure."""
        # Check workflow metadata
        assert deploy_config['name'] == 'Deploy to Production'
        
        # Check trigger conditions
        assert 'push' in deploy_config['on']
        assert 'branches' in deploy_config['on']['push']
        assert 'main' in deploy_config['on']['push']['branches']
        
        # Check job dependencies
        deploy_job = deploy_config['jobs']['deploy']
        assert deploy_job['needs'] == 'build-and-push'
        assert deploy_job['if'] == "github.event_name == 'push' && github.ref == 'refs/heads/main'"
    
    def test_deploy_workflow_secrets(self, deploy_config: Dict[str, Any]):
        """Test that all required secrets are used in the workflow."""
        deploy_job = deploy_config['jobs']['deploy']
        script_steps = [step for step in deploy_job['steps'] if 'uses' in step and 'ssh-action' in step['uses']]
        
        assert len(script_steps) > 0, "No SSH action step found in deploy job"
        
        ssh_step = script_steps[0]
        required_secrets = ['PROD_SERVER_IP', 'PROD_SERVER_USER', 'PROD_SSH_KEY']
        
        for secret in required_secrets:
            assert f'${{{{ secrets.{secret} }}}}' in str(ssh_step), f"Missing secret: {secret}"
    
    @pytest.mark.integration
    @pytest.mark.docker
    def test_docker_commands_locally(self, tmp_path: Path):
        """Test Docker commands with a test container."""
        client = docker.from_env()
        
        try:
            # Test docker pull with a small image
            image_name = "alpine:latest"
            result = client.images.pull(image_name)
            assert result is not None
            
            # Test container lifecycle
            container = client.containers.run(
                image_name,
                command="echo 'Test container started'",
                detach=True,
                remove=True
            )
            
            # Give container time to start and complete
            time.sleep(2)
            
            # Verify container ran successfully
            assert container.status in ['created', 'exited']
            
            # Test docker system prune
            pruned = client.containers.prune()
            assert 'SpaceReclaimed' in pruned
            
        finally:
            # Cleanup
            client.containers.prune()
            client.images.prune(filters={'dangling': False})
    
    @pytest.mark.integration
    def test_deployment_script_permissions(self, deploy_file_path: Path):
        """Test that the deployment script has correct permissions."""
        # Check that the file is readable and has correct permissions
        assert os.access(deploy_file_path, os.R_OK), "Deploy file is not readable"
        
        # Check that the file is a regular file
        assert deploy_file_path.is_file(), "Deploy file is not a regular file"
        
        # Check file extension
        assert deploy_file_path.suffix in ['.yml', '.yaml'], "Deploy file has incorrect extension"
    
    @pytest.mark.parametrize("env_var, expected_value", [
        ("DOCKER_IMAGE", "your-docker-username/synova-ai"),
        ("DOCKER_TAG", "${{ github.sha }}")
    ])
    def test_environment_variables(self, deploy_config: Dict[str, Any], env_var: str, expected_value: str):
        """Test that required environment variables are set."""
        assert env_var in deploy_config['env'], f"Missing environment variable: {env_var}"
        assert deploy_config['env'][env_var] == expected_value, \
            f"Incorrect value for {env_var}. Expected {expected_value}, got {deploy_config['env'][env_var]}"
