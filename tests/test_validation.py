#!/usr/bin/env python3
"""
Test validation script functionality.
"""

import json
import yaml
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from validate_submission import SubmissionValidator


def test_valid_json():
    """Test validation of valid JSON file."""
    validator = SubmissionValidator(['username', 'data', 'timestamp'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'data': {'key': 'value'},
            'timestamp': '2024-01-20T10:30:00Z'
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"Expected valid, got errors: {errors}"
    assert len(errors) == 0
    print("✅ Valid JSON test passed")


def test_valid_yaml():
    """Test validation of valid YAML file."""
    validator = SubmissionValidator(['username', 'data', 'timestamp'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            'username': 'test_user',
            'data': {'key': 'value'},
            'timestamp': '2024-01-20T10:30:00Z'
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"Expected valid, got errors: {errors}"
    assert len(errors) == 0
    print("✅ Valid YAML test passed")


def test_missing_required_field():
    """Test validation with missing required field."""
    validator = SubmissionValidator(['username', 'data', 'timestamp'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'data': {'key': 'value'}
            # Missing timestamp
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("timestamp" in error for error in errors)
    print("✅ Missing required field test passed")


def test_invalid_username():
    """Test validation with invalid username."""
    validator = SubmissionValidator(['username', 'data', 'timestamp'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test@user!',  # Invalid characters
            'data': {'key': 'value'},
            'timestamp': '2024-01-20T10:30:00Z'
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("username" in error.lower() for error in errors)
    print("✅ Invalid username test passed")


def test_invalid_json():
    """Test validation with invalid JSON format."""
    validator = SubmissionValidator(['username', 'data', 'timestamp'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{ invalid json }')
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("JSON" in error for error in errors)
    print("✅ Invalid JSON format test passed")


def test_empty_required_field():
    """Test validation with empty required field."""
    validator = SubmissionValidator(['username', 'data', 'timestamp'])
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': '',  # Empty username
            'data': {'key': 'value'},
            'timestamp': '2024-01-20T10:30:00Z'
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("username" in error.lower() and "empty" in error.lower() for error in errors)
    print("✅ Empty required field test passed")


def main():
    """Run all tests."""
    print("Running validation tests...\n")
    
    tests = [
        test_valid_json,
        test_valid_yaml,
        test_missing_required_field,
        test_invalid_username,
        test_invalid_json,
        test_empty_required_field
    ]
    
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            return 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            return 1
    
    print("\n✅ All tests passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())