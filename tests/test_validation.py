#!/usr/bin/env python3
"""
Test validation script functionality with new fields.
"""

import json
import yaml
import tempfile
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from validate_submission import SubmissionValidator


def test_valid_json_full():
    """Test validation of valid JSON file with all fields."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'data_url': 'https://example.com/data',
            'claims': [
                {
                    'claim': 'Test claim 1',
                    'context': 'Under specific conditions',
                    'instruction': ['Step 1', 'Step 2']
                },
                {
                    'claim': 'Test claim 2',
                    'instruction': ['Step 1', 'Step 2', 'Step 3']
                }
            ],
            'non_reproducible_claims': [
                {
                    'claim': 'Non-reproducible claim',
                    'reason': 'Requires physical equipment'
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"Expected valid, got errors: {errors}"
    assert len(errors) == 0
    print("✅ Valid JSON with all fields test passed")


def test_valid_yaml_minimal():
    """Test validation of valid YAML file with minimal required fields."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['Step 1', 'Step 2']
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"Expected valid, got errors: {errors}"
    assert len(errors) == 0
    print("✅ Valid YAML with minimal fields test passed")


def test_pip_libraries_no_code_url():
    """Test validation with pip_libraries claim type (code_url optional)."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'pip_libraries',
            # No code_url - should be valid for pip_libraries
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['pip install numpy', 'python script.py']
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"Expected valid for pip_libraries without code_url, got errors: {errors}"
    assert len(errors) == 0
    print("✅ pip_libraries without code_url test passed")


def test_custom_code_requires_url():
    """Test validation with custom_code claim type requires code_url."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            # Missing code_url - should fail for custom_code
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['Step 1']
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("code_url" in error for error in errors)
    print("✅ custom_code requires code_url test passed")


def test_missing_required_field():
    """Test validation with missing required field."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            # Missing paper_title
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['Step 1']
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("paper_title" in error for error in errors)
    print("✅ Missing required field test passed")


def test_invalid_username():
    """Test validation with invalid username."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test@user!',  # Invalid characters
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['Step 1']
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("username" in error.lower() for error in errors)
    print("✅ Invalid username test passed")


def test_empty_claims_list():
    """Test validation with empty claims list."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'claims': []  # Empty list
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("at least one claim" in error.lower() for error in errors)
    print("✅ Empty claims list test passed")


def test_claim_missing_instruction():
    """Test validation with claim missing instruction field."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'claims': [
                {
                    'claim': 'Test claim'
                    # Missing instruction
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("instruction" in error for error in errors)
    print("✅ Claim missing instruction test passed")


def test_optional_context_field():
    """Test that context field is properly handled as optional."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'claims': [
                {
                    'claim': 'Test claim with context',
                    'context': 'Valid context string',
                    'instruction': ['Step 1']
                },
                {
                    'claim': 'Test claim without context',
                    'instruction': ['Step 1']
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"Context field should be optional, got errors: {errors}"
    print("✅ Optional context field test passed")


def test_non_reproducible_claims_optional():
    """Test that non_reproducible_claims is optional."""
    validator = SubmissionValidator()
    
    # Test without non_reproducible_claims
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['Step 1']
                }
            ]
            # No non_reproducible_claims field
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"non_reproducible_claims should be optional, got errors: {errors}"
    print("✅ Optional non_reproducible_claims test passed")


def test_non_reproducible_claims_with_reason():
    """Test non_reproducible_claims with and without reason."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'custom_code',
            'code_url': 'https://github.com/test/repo',
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['Step 1']
                }
            ],
            'non_reproducible_claims': [
                {
                    'claim': 'Claim with reason',
                    'reason': 'Valid reason'
                },
                {
                    'claim': 'Claim without reason'
                    # Should generate warning but not error
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert is_valid, f"Should be valid even without reason, got errors: {errors}"
    assert len(warnings) > 0, "Should have warning for missing reason"
    assert any("reason" in warning for warning in warnings)
    print("✅ Non-reproducible claims reason test passed")


def test_invalid_claim_type():
    """Test validation with invalid claim_type."""
    validator = SubmissionValidator()
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({
            'username': 'test_user',
            'paper_title': 'Test Paper Title',
            'paper_pdf': 'https://example.com/paper.pdf',
            'identifier': '10.1234/example',
            'claim_type': 'invalid_type',  # Invalid claim type
            'code_url': 'https://github.com/test/repo',
            'claims': [
                {
                    'claim': 'Test claim',
                    'instruction': ['Step 1']
                }
            ]
        }, f)
        f.flush()
        
        is_valid, errors, warnings = validator.validate_file(f.name)
        os.unlink(f.name)
    
    assert not is_valid
    assert any("claim_type" in error for error in errors)
    print("✅ Invalid claim_type test passed")


def main():
    """Run all tests."""
    print("Running validation tests with new fields...\n")
    
    tests = [
        test_valid_json_full,
        test_valid_yaml_minimal,
        test_pip_libraries_no_code_url,
        test_custom_code_requires_url,
        test_missing_required_field,
        test_invalid_username,
        test_empty_claims_list,
        test_claim_missing_instruction,
        test_optional_context_field,
        test_non_reproducible_claims_optional,
        test_non_reproducible_claims_with_reason,
        test_invalid_claim_type
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