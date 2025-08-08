"""
Pytest configuration and shared fixtures for pyavrocd tests.
"""
import pytest
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_device():
    """Sample device name for testing."""
    return "attiny85"

@pytest.fixture
def sample_interface():
    """Sample interface for testing."""
    return "debugwire"

@pytest.fixture
def mock_args():
    """Mock command line arguments for testing."""
    class MockArgs:
        def __init__(self):
            self.dev = "attiny85"
            self.interface = "debugwire"
            self.tool = "edbg"
            self.port = 2000
            self.verbose = "info"
            self.serialnumber = None
            self.cmd = None
            self.gede = False
            self.prg = None
            self.version = False

    return MockArgs()

# Configure pytest marks
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "hardware: mark test as requiring hardware connection"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
