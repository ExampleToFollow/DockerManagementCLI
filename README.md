# DockerManagementCLI

Interactive command-line interface for comprehensive Docker container and image management with menu-driven navigation and streamlined operations.

[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Table of Contents

- [Installation](#installation)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Features](#features)
- [Usage Examples](#usage-examples)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Error Handling](#error-handling)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Standard Installation
```bash
git clone https://github.com/username/DockerManagementCLI.git
cd DockerManagementCLI
chmod +x DockerManagementCLI.py
```

### System-wide Installation
```bash
sudo cp DockerManagementCLI.py /usr/local/bin/docker-cli
sudo chmod +x /usr/local/bin/docker-cli
```

### Development Installation
```bash
git clone https://github.com/username/DockerManagementCLI.git
cd DockerManagementCLI
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Requirements

### System Requirements
- **Python**: 3.6 or higher
- **Docker Engine**: 20.10 or higher
- **Operating System**: Linux, macOS, Windows (WSL2)
- **Memory**: Minimum 512MB available RAM
- **Disk Space**: 50MB for installation

### Python Dependencies
```python
# Standard library only - no external dependencies required
import subprocess
import sys
import json
import os
from typing import List, Dict, Optional
```

### Docker Permissions
```bash
# Add user to docker group (Linux/macOS)
sudo usermod -aG docker $USER
newgrp docker

# Verify permissions
docker ps
```

## Quick Start

### Basic Execution
```bash
python3 DockerManagementCLI.py
```

### Verify Installation
```bash
# Check Docker availability
docker --version

# Test Docker daemon connection
docker info

# Run the CLI
python3 DockerManagementCLI.py
```

## Features

### Image Management Operations

| Operation | Description | Docker Equivalent |
|-----------|-------------|------------------|
| **List Images** | Display all local Docker images with size and creation date | `docker images --format table` |
| **Pull Image** | Download images from Docker registries with progress tracking | `docker pull <image>:<tag>` |
| **Build Image** | Build images from Dockerfile with custom naming | `docker build -t <name> <path>` |
| **Remove Image** | Delete images with safety confirmation and dependency checks | `docker rmi <image>` |

### Container Management Operations

| Operation | Description | Docker Equivalent |
|-----------|-------------|------------------|
| **List Containers** | View active containers or all containers with detailed status | `docker ps` / `docker ps -a` |
| **Run Container** | Create and start containers with port mapping and naming | `docker run -d --name <name> -p <port>:<port> <image>` |
| **Start Container** | Start stopped containers with status verification | `docker start <container>` |
| **Stop Container** | Gracefully stop running containers with timeout handling | `docker stop <container>` |
| **Restart Container** | Restart containers with automatic health checks | `docker restart <container>` |
| **Remove Container** | Delete containers with force option for running containers | `docker rm -f <container>` |
| **View Logs** | Display container logs with tail option and real-time output | `docker logs --tail 50 <container>` |
| **Execute Shell** | Interactive shell access to running containers | `docker exec -it <container> /bin/bash` |

### System Management Operations

| Operation | Description | Docker Equivalent |
|-----------|-------------|------------------|
| **System Info** | Comprehensive Docker system information and configuration | `docker system info` |
| **Disk Usage** | Detailed breakdown of Docker disk space utilization | `docker system df` |
| **System Cleanup** | Remove unused containers, networks, images, and build cache | `docker system prune -a -f` |

## Usage Examples

### Container Deployment Workflow
```bash
# 1. Launch CLI
python3 DockerManagementCLI.py

# 2. Pull base image
# Menu: Image Management → Pull Image
# Input: nginx:alpine

# 3. Run container with port mapping
# Menu: Container Management → Run Container
# Image: nginx:alpine
# Name: web-server
# Ports: 8080:80

# 4. Verify deployment
# Menu: Container Management → List Active Containers
```

### Development Environment Setup
```bash
# Database container
# Image: postgres:13
# Name: dev-db
# Ports: 5432:5432

# Application container
# Image: openjdk:11
# Name: spring-app
# Ports: 8080:8080

# Monitor all services
# Menu: Container Management → List All Containers
# Menu: Container Management → View Logs
```

### Maintenance Operations
```bash
# Check system resources
# Menu: System Management → Disk Usage

# Clean unused resources
# Menu: System Management → System Cleanup

# Verify cleanup results
# Menu: System Management → System Info
```

## Architecture

### Class Structure
```python
DockerCLI                    # Main CLI interface and menu system
├── DockerManager           # Core Docker command execution and validation
├── ImageManager            # Image lifecycle and registry operations  
├── ContainerManager        # Container lifecycle and runtime operations
└── SystemManager           # System monitoring, cleanup, and diagnostics
```

### Component Responsibilities

#### DockerManager
- Docker installation verification
- Command execution with error handling
- Interactive and non-interactive command support
- Process management and output capture

#### ImageManager
- Image listing with formatted output
- Registry operations (pull/push)
- Dockerfile-based image building
- Image removal with dependency validation

#### ContainerManager
- Container lifecycle management
- Port mapping and network configuration
- Log aggregation and monitoring
- Interactive shell session management

#### SystemManager
- Resource utilization monitoring
- System diagnostics and health checks
- Automated cleanup operations
- Performance metrics collection

## API Reference

### DockerManager Methods

```python
check_docker_installed() -> None
    """Verifies Docker installation and accessibility"""

run_command(command: List[str]) -> Optional[str]
    """Executes Docker command and returns output"""

run_command_interactive(command: List[str]) -> bool
    """Executes interactive Docker command"""
```

### ImageManager Methods

```python
list_images() -> None
    """Displays formatted table of all Docker images"""

pull_image() -> None
    """Interactive image download from registry"""

build_image() -> None
    """Build image from Dockerfile with custom configuration"""

remove_image() -> None
    """Remove image with safety confirmation"""
```

### ContainerManager Methods

```python
list_containers(all_containers: bool = True) -> None
    """List containers with optional filtering"""

run_container() -> None
    """Create and start new container with configuration"""

start_container() -> None
stop_container() -> None
restart_container() -> None
    """Container lifecycle management operations"""

remove_container() -> None
    """Remove container with force option"""

view_logs() -> None
    """Display container logs with tail option"""

exec_container() -> None
    """Execute interactive shell in container"""
```

### SystemManager Methods

```python
system_info() -> None
    """Display comprehensive Docker system information"""

disk_usage() -> None
    """Show Docker disk space utilization"""

system_cleanup() -> None
    """Clean unused Docker resources"""
```

## Configuration

### Environment Variables
```bash
# Optional: Docker host configuration
export DOCKER_HOST=unix:///var/run/docker.sock

# Optional: Docker API version
export DOCKER_API_VERSION=1.41

# Optional: Default registry
export DOCKER_REGISTRY=docker.io
```

### Runtime Configuration
- No external configuration files required
- All settings managed through interactive prompts
- Automatic detection of Docker daemon settings
- Platform-specific path resolution

## Error Handling

### Input Validation
- Empty input detection and user prompts
- Container/image ID format validation
- Port mapping syntax verification
- File path existence checks

### Docker Command Errors
- Connection failure to Docker daemon
- Permission denied operations
- Resource not found scenarios
- Network connectivity issues

### Recovery Mechanisms
- Graceful error reporting with actionable messages
- Automatic retry for transient failures
- Safe operation cancellation
- State consistency validation

### Error Categories

```python
# Connection Errors
ConnectionError: Docker daemon not accessible
PermissionError: Insufficient Docker permissions

# Resource Errors  
NotFoundError: Container/image not found
ConflictError: Resource name conflicts

# Operation Errors
TimeoutError: Operation timeout exceeded
ValidationError: Invalid input parameters
```

## Troubleshooting

### Common Issues

#### Docker Not Found
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Verify installation
docker --version
```

#### Permission Denied
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Restart session
logout
# login again

# Test permissions
docker ps
```

#### Python Version Issues
```bash
# Check Python version
python3 --version

# Install Python 3.6+
sudo apt update
sudo apt install python3.8

# Verify installation
python3.8 DockerManagementCLI.py
```

#### Docker Daemon Not Running
```bash
# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Check service status
sudo systemctl status docker
```

### Debug Mode
```bash
# Enable verbose Docker output
export DOCKER_BUILDKIT=0

# Run with Python debugging
python3 -u DockerManagementCLI.py

# Check Docker daemon logs
sudo journalctl -u docker.service -f
```

### Performance Optimization
```bash
# Clean Docker system regularly
docker system prune -a -f

# Monitor resource usage
docker stats

# Optimize Docker daemon
sudo vim /etc/docker/daemon.json
```

## Contributing

### Development Setup
```bash
git clone https://github.com/username/DockerManagementCLI.git
cd DockerManagementCLI

# Create development branch
git checkout -b feature/new-feature

# Make changes and test
python3 DockerManagementCLI.py

# Commit changes
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### Code Style Guidelines
- Follow PEP 8 Python style guide
- Use type hints for all function parameters
- Include comprehensive docstrings
- Implement error handling for all operations
- Add unit tests for new functionality

### Testing Requirements
```bash
# Run basic functionality tests
python3 -m pytest tests/

# Test Docker integration
python3 tests/integration_test.py

# Performance benchmarks
python3 tests/performance_test.py
```

### Contribution Workflow
1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request with detailed description

## License

```
MIT License

Copyright (c) 2025 DockerManagementCLI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
