"""Tests for the metadata package initialization."""

import pytest

def test_metadata_imports():
    """Test that all components are properly exported from the metadata package."""
    # Import the metadata package
    import opendbc.metadata as metadata
    
    # Test constants
    assert hasattr(metadata, 'COLUMNS')
    assert hasattr(metadata, 'EXTRA_CARS_COLUMNS')
    assert hasattr(metadata, 'STARS')
    assert hasattr(metadata, 'SUPPORT_TYPES')
    assert hasattr(metadata, 'MS_TO_MPH')
    assert hasattr(metadata, 'GOOD_TORQUE_THRESHOLD')
    
    # Test parts
    assert hasattr(metadata, 'Part')
    assert hasattr(metadata, 'Tool')
    assert hasattr(metadata, 'CarParts')
    assert hasattr(metadata, 'PlatformParts')
    assert hasattr(metadata, 'BrandPartProcessor')
    assert hasattr(metadata, 'PartCategory')
    
    # Test footnotes
    assert hasattr(metadata, 'Footnote')
    assert hasattr(metadata, 'FootnoteCollection')
    
    # Test processors
    assert hasattr(metadata, 'BaseProcessor')
    assert hasattr(metadata, 'ModelData')
    assert hasattr(metadata, 'SubaruProcessor')
    assert hasattr(metadata, 'HyundaiProcessor')
    
    # Test parts definitions
    assert hasattr(metadata, 'Harness')
    assert hasattr(metadata, 'ToolEnum')
    assert hasattr(metadata, 'Kit')
    assert hasattr(metadata, 'Accessory')
    assert hasattr(metadata, 'Category')
    assert hasattr(metadata, 'BasePart')
    assert hasattr(metadata, 'EnumBase')
    assert hasattr(metadata, 'get_part_by_name')
    assert hasattr(metadata, 'get_all_parts')

def test_flag_based_processor_import():
    """Test that the flag-based processor is properly exported if available."""
    try:
        # Try to import the flag-based processor directly
        from opendbc.metadata.base.flag_processor import FlagBasedProcessor, FlagConfig
        
        # If we get here, the flag-based processor is available, so check if it's exported
        import opendbc.metadata as metadata
        assert hasattr(metadata, 'FlagBasedProcessor')
        assert hasattr(metadata, 'FlagConfig')
    except ImportError:
        # Flag-based processor is not available, skip the test
        pytest.skip("FlagBasedProcessor not available") 