"""Tests for the metadata framework directory structure."""

import os
import pytest

def test_directory_structure():
    """Test that the directory structure is set up correctly with only needed files."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # Required directories
    required_dirs = [
        "opendbc/metadata",                                      # Root package for metadata framework
        "opendbc/metadata/base",                                 # Base components shared across brands
        "opendbc/metadata/brand_metadata",                       # Brand-specific implementations
        "opendbc/metadata/brand_metadata/subaru",                # Subaru implementation
        "opendbc/metadata/brand_metadata/hyundai",               # Hyundai implementation
        "opendbc/metadata/tests",                                # Test directory
        "opendbc/metadata/tests/test_base",                      # Tests for base components
        "opendbc/metadata/tests/test_brand_metadata",            # Tests for brand implementations
        "opendbc/metadata/tests/test_brand_metadata/test_subaru", # Tests for Subaru implementation
        "opendbc/metadata/tests/test_brand_metadata/test_hyundai", # Tests for Hyundai implementation
    ]
    
    # Required base files
    required_base_files = [
        "opendbc/metadata/__init__.py",                          # Package exports and documentation
        "opendbc/metadata/base/__init__.py",                     # Base package exports
        "opendbc/metadata/base/constants.py",                    # Constants used throughout the framework
        "opendbc/metadata/base/parts.py",                        # Core part data structures
        "opendbc/metadata/base/footnotes.py",                    # Footnote data structures
        "opendbc/metadata/base/processor.py",                    # Base processor for metadata
        "opendbc/metadata/base/flag_processor.py",               # Flag-based processor for metadata
        "opendbc/metadata/base/parts_catalog.py",                # Central catalog of parts
    ]
    
    # Required brand files (Subaru and Hyundai implementations)
    required_brand_files = [
        "opendbc/metadata/brand_metadata/__init__.py",           # Brand metadata package exports
        "opendbc/metadata/brand_metadata/subaru/__init__.py",    # Subaru package exports
        "opendbc/metadata/brand_metadata/subaru/processor.py",   # Subaru-specific processor
        "opendbc/metadata/brand_metadata/subaru/attributes.py",  # Subaru-specific attributes
        "opendbc/metadata/brand_metadata/subaru/footnotes.py",   # Subaru-specific footnotes
        "opendbc/metadata/brand_metadata/hyundai/__init__.py",   # Hyundai package exports
        "opendbc/metadata/brand_metadata/hyundai/processor.py",  # Hyundai-specific processor
        "opendbc/metadata/brand_metadata/hyundai/attributes.py", # Hyundai-specific attributes
    ]
    
    # Required test files
    required_test_files = [
        "opendbc/metadata/tests/__init__.py",                    # Test package initialization
        "opendbc/metadata/tests/test_structure.py",              # Tests for directory structure
        "opendbc/metadata/tests/test_init.py",                   # Tests for package exports
        "opendbc/metadata/tests/test_base/__init__.py",          # Base tests package
        "opendbc/metadata/tests/test_base/test_constants.py",    # Tests for constants
        "opendbc/metadata/tests/test_base/test_parts.py",        # Tests for parts
        "opendbc/metadata/tests/test_base/test_footnotes.py",    # Tests for footnotes
        "opendbc/metadata/tests/test_base/test_processor.py",    # Tests for processor
        "opendbc/metadata/tests/test_base/test_parts_catalog.py", # Tests for parts catalog
        "opendbc/metadata/tests/test_brand_metadata/__init__.py", # Brand tests package
        "opendbc/metadata/tests/test_brand_metadata/test_parts_integration.py", # Tests for parts integration
        "opendbc/metadata/tests/test_brand_metadata/test_subaru/__init__.py",   # Subaru tests package
        "opendbc/metadata/tests/test_brand_metadata/test_subaru/test_processor.py", # Tests for Subaru processor
        "opendbc/metadata/tests/test_brand_metadata/test_subaru/test_footnotes.py", # Tests for Subaru footnotes
        "opendbc/metadata/tests/test_brand_metadata/test_hyundai/__init__.py",      # Hyundai tests package
        "opendbc/metadata/tests/test_brand_metadata/test_hyundai/test_processor.py", # Tests for Hyundai processor
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
