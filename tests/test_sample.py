"""
Simple test to verify the pytest configuration is working.
"""
import pytest

def test_basic_addition():
    """Test basic addition."""
    assert 1 + 1 == 2

def test_basic_subtraction():
    """Test basic subtraction."""
    assert 5 - 3 == 2

@pytest.mark.unit
def test_string_operations():
    """Test string operations."""
    result = "hello" + " " + "world"
    assert result == "hello world"
    assert len(result) == 11

@pytest.mark.slow
def test_slow_operation():
    """Test marked as slow."""
    import time
    time.sleep(0.1)  # Simulate slow operation
    assert True
