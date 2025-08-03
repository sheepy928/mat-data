#!/usr/bin/env python3
"""
Validate submission files for crowdsourcing data collection.
"""

import json
import yaml
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any


class SubmissionValidator:
    def __init__(self, required_fields: List[str] = None):
        # Default required fields for materials science papers
        self.required_fields = required_fields or [
            'username', 'paper_title', 'paper_pdf', 'identifier', 'claim_type', 'claims'
        ]
        self.errors = []
        self.warnings = []
    
    def validate_file(self, filepath: str) -> Tuple[bool, List[str], List[str]]:
        """Validate a single submission file."""
        self.errors = []
        self.warnings = []
        
        if not os.path.exists(filepath):
            self.errors.append(f"File not found: {filepath}")
            return False, self.errors, self.warnings
        
        # Check file extension
        file_ext = Path(filepath).suffix.lower()
        if file_ext not in ['.json', '.yaml', '.yml']:
            self.errors.append(f"Invalid file extension: {file_ext}. Must be .json, .yaml, or .yml")
            return False, self.errors, self.warnings
        
        # Load and validate content
        try:
            if file_ext == '.json':
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON format: {e}")
            return False, self.errors, self.warnings
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML format: {e}")
            return False, self.errors, self.warnings
        except Exception as e:
            self.errors.append(f"Error reading file: {e}")
            return False, self.errors, self.warnings
        
        # Validate required fields
        if not isinstance(data, dict):
            self.errors.append("Data must be a JSON/YAML object (dictionary)")
            return False, self.errors, self.warnings
        
        for field in self.required_fields:
            if field not in data:
                self.errors.append(f"Required field missing: '{field}'")
            elif data[field] is None or (isinstance(data[field], str) and not data[field].strip()):
                self.errors.append(f"Required field '{field}' cannot be empty")
        
        # Additional validations
        self._validate_data_structure(data)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_data_structure(self, data: Dict[str, Any]):
        """Validate materials science paper data structure."""
        # Validate username format
        if 'username' in data:
            username = str(data['username']).strip()
            if not username:
                self.errors.append("Username cannot be empty")
            elif not username.replace('-', '').replace('_', '').isalnum():
                self.errors.append("Username can only contain letters, numbers, hyphens, and underscores")
            elif len(username) > 39:  # GitHub username limit
                self.errors.append("Username is too long (max 39 characters)")
        
        # Validate claim_type
        if 'claim_type' in data:
            claim_type = str(data['claim_type']).strip()
            if claim_type not in ['custom_code', 'pip_libraries']:
                self.errors.append("claim_type must be either 'custom_code' or 'pip_libraries'")
            
            # Check code_url requirement based on claim_type
            if claim_type == 'custom_code' and not data.get('code_url'):
                self.errors.append("code_url is required for custom_code claim type")
        else:
            # If claim_type is missing, assume it requires code_url for backward compatibility
            if not data.get('code_url'):
                self.errors.append("code_url is required (or specify claim_type as 'pip_libraries' if using standard libraries)")
        
        # Validate paper_title
        if 'paper_title' in data:
            if not isinstance(data['paper_title'], str) or not data['paper_title'].strip():
                self.errors.append("Paper title must be a non-empty string")
        
        # Validate URLs
        url_fields = ['paper_pdf', 'code_url', 'data_url']
        for field in url_fields:
            if field in data and data[field]:
                url = str(data[field]).strip()
                if not url.startswith(('http://', 'https://')):
                    self.errors.append(f"{field} must be a valid URL starting with http:// or https://")
        
        # Validate identifier (e.g., arxiv ID)
        if 'identifier' in data:
            identifier = str(data['identifier']).strip()
            if not identifier:
                self.errors.append("Identifier cannot be empty")
        
        # Validate claims structure
        if 'claims' in data:
            if not isinstance(data['claims'], list):
                self.errors.append("Claims must be a list")
            elif not data['claims']:
                self.errors.append("At least one claim is required")
            else:
                for i, claim in enumerate(data['claims']):
                    if not isinstance(claim, dict):
                        self.errors.append(f"Claim {i+1} must be a dictionary")
                    else:
                        if 'claim' not in claim or not str(claim['claim']).strip():
                            self.errors.append(f"Claim {i+1} must have a non-empty 'claim' field")
                        if 'instruction' not in claim:
                            self.errors.append(f"Claim {i+1} must have an 'instruction' field")
                        elif not isinstance(claim['instruction'], list):
                            self.errors.append(f"Claim {i+1} 'instruction' field must be a list of strings")
                        elif not claim['instruction']:
                            self.errors.append(f"Claim {i+1} 'instruction' list cannot be empty")
                        else:
                            for j, step in enumerate(claim['instruction']):
                                if not isinstance(step, str) or not step.strip():
                                    self.errors.append(f"Claim {i+1} instruction step {j+1} must be a non-empty string")


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_submission.py <file_path> [required_field1] [required_field2] ...")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    # Override with command line arguments if provided
    required_fields = None
    if len(sys.argv) > 2:
        required_fields = sys.argv[2:]
    
    validator = SubmissionValidator(required_fields)
    is_valid, errors, warnings = validator.validate_file(filepath)
    
    # Print results
    if errors:
        print("VALIDATION ERRORS:")
        for error in errors:
            print(f"  ❌ {error}")
    
    if warnings:
        print("\nWARNINGS:")
        for warning in warnings:
            print(f"  ⚠️  {warning}")
    
    if is_valid:
        print("\n✅ Validation passed!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()