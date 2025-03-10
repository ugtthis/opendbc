import os
import pytest

def test_directory_structure():
    """Test that the directory structure is set up correctly."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    # Check main directories
    assert os.path.isdir(os.path.join(project_root, "opendbc/metadata"))
    assert os.path.isdir(os.path.join(project_root, "opendbc/metadata/base"))
    assert os.path.isdir(os.path.join(project_root, "opendbc/metadata/utils"))
    assert os.path.isdir(os.path.join(project_root, "opendbc/metadata/brand_metadata"))
    assert os.path.isdir(os.path.join(project_root, "opendbc/metadata/brand_metadata/subaru"))
    assert os.path.isdir(os.path.join(project_root, "opendbc/metadata/tests"))
    
    # Check key files
    assert os.path.isfile(os.path.join(project_root, "opendbc/metadata/__init__.py"))
    assert os.path.isfile(os.path.join(project_root, "opendbc/metadata/base/constants.py"))
    assert os.path.isfile(os.path.join(project_root, "opendbc/metadata/base/parts.py"))
    assert os.path.isfile(os.path.join(project_root, "opendbc/metadata/base/footnotes.py"))
    assert os.path.isfile(os.path.join(project_root, "opendbc/metadata/base/processor.py"))
    assert os.path.isfile(os.path.join(project_root, "opendbc/metadata/utils/parsing.py"))
    assert os.path.isfile(os.path.join(project_root, "opendbc/metadata/docs_generator.py"))
