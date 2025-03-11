"""Tests for the metadata framework directory structure."""

import os
import pytest

def test_directory_structure():
    """Test that the directory structure is set up correctly with only needed files."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # Required directories
    required_dirs = [
        "opendbc/metadata",
        "opendbc/metadata/base",
        "opendbc/metadata/brand_metadata",
        "opendbc/metadata/brand_metadata/subaru",  # First brand implementation
        "opendbc/metadata/brand_metadata/hyundai",  # Second brand implementation
        "opendbc/metadata/tests",
        "opendbc/metadata/tests/test_base",
        "opendbc/metadata/tests/test_brand_metadata",
        "opendbc/metadata/tests/test_brand_metadata/test_subaru",
        "opendbc/metadata/tests/test_brand_metadata/test_hyundai",
    ]
    
    # Required base files
    required_base_files = [
        "opendbc/metadata/__init__.py",
        "opendbc/metadata/base/__init__.py",
        "opendbc/metadata/base/constants.py",
        "opendbc/metadata/base/parts.py",
        "opendbc/metadata/base/footnotes.py",
        "opendbc/metadata/base/processor.py",
    ]
    
    # Required brand files (Subaru and Hyundai implementations)
    required_brand_files = [
        "opendbc/metadata/brand_metadata/__init__.py",
        "opendbc/metadata/brand_metadata/subaru/__init__.py",
        "opendbc/metadata/brand_metadata/subaru/processor.py",
        "opendbc/metadata/brand_metadata/subaru/attributes.py",  # For brand-specific metadata
        "opendbc/metadata/brand_metadata/subaru/footnotes.py",  # For brand-specific footnotes
        "opendbc/metadata/brand_metadata/hyundai/__init__.py",
        "opendbc/metadata/brand_metadata/hyundai/processor.py",
    ]
    
    # Required test files
    required_test_files = [
        "opendbc/metadata/tests/__init__.py",
        "opendbc/metadata/tests/test_structure.py",
        "opendbc/metadata/tests/test_base/__init__.py",
        "opendbc/metadata/tests/test_base/test_constants.py",
        "opendbc/metadata/tests/test_base/test_parts.py",
        "opendbc/metadata/tests/test_base/test_footnotes.py",
        "opendbc/metadata/tests/test_base/test_processor.py",
        "opendbc/metadata/tests/test_brand_metadata/__init__.py",
        "opendbc/metadata/tests/test_brand_metadata/test_subaru/__init__.py",
        "opendbc/metadata/tests/test_brand_metadata/test_subaru/test_processor.py",
        "opendbc/metadata/tests/test_brand_metadata/test_subaru/test_footnotes.py",
        "opendbc/metadata/tests/test_brand_metadata/test_hyundai/__init__.py",
        "opendbc/metadata/tests/test_brand_metadata/test_hyundai/test_processor.py",
    ]
    
    # Check all required directories exist
    for directory in required_dirs:
        path = os.path.join(project_root, directory)
        assert os.path.isdir(path), f"Required directory missing: {directory}"
    
    # Check all required files exist
    for file_path in required_base_files + required_brand_files + required_test_files:
        path = os.path.join(project_root, file_path)
        assert os.path.isfile(path), f"Required file missing: {file_path}"
    
    # Check no extra files exist in metadata directory
    def check_no_extra_files(directory, required_files):
        dir_path = os.path.join(project_root, directory)
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(os.path.relpath(root, project_root), file)
                    assert file_path in required_files, f"Extra file found: {file_path}"
    
    all_required_files = required_base_files + required_brand_files + required_test_files
    check_no_extra_files('opendbc/metadata', all_required_files)
